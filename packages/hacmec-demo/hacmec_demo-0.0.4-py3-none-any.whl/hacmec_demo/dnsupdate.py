"""
Utils for DNS-01 method
"""

import logging
from collections import deque
from dataclasses import dataclass
from time import sleep
from typing import Mapping, Set

import dns.name
import dns.query
import dns.resolver
import dns.tsigkeyring
import dns.update


def strip_zone(fqdn: str, zone: str) -> str:
    """
    Compute host part of an fqdn given a zone.
    E.g. "foo.bar.example.org", "example.org." ==> "foo.bar"
    """
    fqdn = fqdn.rstrip('.')
    zone = zone.rstrip('.')
    if not fqdn.endswith(zone):
        raise ValueError(f'{fqdn!r} is not in zone {zone!r}')
    return fqdn[:-len(zone)].rstrip('.')


def update_txt(
        nserver: str,
        key_name: str,
        secret: str,
        hmac_algo: str,
        zone: str,
        records: Mapping[str, str],
        ttl: int,
) -> None:
    """
    Upsert TXT records through TSIG authenticated dns update request.

    nserver: DNS server to send update to.
    key_name: Name of shared key
    secret: Shared secret (b64 string)
    hmac_algo: hmac algorithm to use for signing
    zone: DNS zone to update
    records: Map from domain names (fully qualified) to TXT record values.
    ttl: time to live
    """
    update = dns.update.Update(
        zone,
        keyring=dns.tsigkeyring.from_text({
            key_name: secret,
        }),
        keyalgorithm=dns.name.from_text(hmac_algo),
    )

    for fqdn, value in records.items():
        update.replace(strip_zone(fqdn, zone), ttl, 'txt', f'"{value}"')

    dns.query.tcp(update, nserver, timeout=10)


def resolve(name: str, typ: str) -> Set[str]:
    """
    Resolve DNS entries using local DNS.
    E.g. resolve('github.com', 'A') ==> {'140.82.118.3', '140.82.118.4'}
    """
    tries = 30
    logging.info(f'Resolving {name!r} ({typ})')
    while True:
        try:
            response = dns.resolver.query(name, typ, lifetime=5)
            break
        except dns.resolver.NoAnswer:
            response = []
            break
        except Exception as ex:
            tries -= 1
            if not tries:
                raise
            logging.exception(ex)
            sleep(2)
    result = {resp.to_text() for resp in response}
    logging.info(f'  ==> {result}')
    return result


@dataclass
class PollJob:
    """
    Job for poll_dns
    """
    nsip: str
    fqdn: str
    value: str


def poll_dns(zone_records: Mapping[str, Mapping[str, str]], v4: bool = True, v6: bool = False) -> None:
    """
    Poll DNS servers for TXT records.

    zone: Zone the records are in
    records: Map from domain names (fully qualified) to TXT record values.
    v4: query v4 dns servers
    v6: query v6 dns servers
    """

    todo = deque(
        PollJob(nsip, fqdn, value)
        for zone, records in zone_records.items()
        for nsip in {
            nsip
            for ns in resolve(zone, 'NS')
            for nsip in (resolve(ns, 'A') if v4 else set()) | (resolve(ns, 'AAAA') if v6 else set())
        }
        for fqdn, value in records.items()
    )

    for job in todo:
        logging.info(f'Polling: {job}')

    tries = 120
    while todo:
        job = todo.popleft()
        value = resolve_txt(job.fqdn, job.nsip)
        if value == {job.value}:
            logging.info(f'done: {job}')
            continue
        logging.info(f'Not yet ok: {job}')
        todo.append(job)
        tries -= 1
        if not tries:
            raise Exception('Out of tries')
        sleep(5)


def resolve_txt(name: str, server: str) -> Set[str]:
    """
    Resolve TXT records on specific DNS server.

    name: record to resolve
    server: server IP (v4 or v6) to query.
    """
    try:
        resp = dns.query.udp(dns.message.make_query(name, 'TXT'), server, timeout=5).answer
        if not resp:
            return set()
        return {
            answer.to_text()[1:-1]
            for answer in resp[0]
        }
    except Exception as ex:
        logging.exception(ex)
        return set()
