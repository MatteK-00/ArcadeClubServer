import urllib3
import requests

import certifi


def __webSearchNew(upc):
    http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED', # Force certificate check.
    ca_certs=certifi.where(),  # Path to the Certifi bundle.
    )

    # You're ready to make verified HTTPS requests.
    try:
        sito = "http://videogames.pricecharting.com/search?q=" + upc
        r = http.request('GET', sito)

        print r.data
    except urllib3.exceptions.SSLError as e:
        print e