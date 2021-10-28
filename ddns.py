#!/usr/bin/env python3

import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


NJALLA_BASE_URL: str = "https://njal.la/update/"


def create_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount(prefix='https://', adapter=adapter)
    return session


def update_ddns() -> None:
    with open('conf.json', "r") as config_file:
        with create_session() as session:
            config: dict = json.load(config_file)
            domain: str
            subdomains: str
            for domain, subdomains in config.items():
                subdomain: str
                key: str
                for subdomain, key in subdomains.items():
                    _domain = f"{subdomain}.{domain}"
                    url: str = f"{NJALLA_BASE_URL}?h={_domain}&k={key}&auto"

                    print(f"{_domain}: updating dns record...")
                    response: requests.Response = session.get(url=url)
                    if not response:
                        print(f'{_domain} failed to update dns record')
                        continue
                    print(f'{_domain}: dns record updated')


if __name__ == '__main__':
    update_ddns()