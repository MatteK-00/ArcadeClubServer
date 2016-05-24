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

        temp = r.data
        page = temp

        temp = temp.split("Prices")

        titolo = temp[0].split("<title>")[1]

        console = temp[1].split(" | Compare Loose")[0]

        console = console.replace("(", "").replace(")", "").replace(" ", "")

        anno = (page.split("class=\"date\">")[1]).split("<")[0]

        foto = page.split("<img src=\"")[1].split("\"")[0]


    except urllib3.exceptions.SSLError as e:
        print e

    print "nome:", titolo
    print "anno:", anno
    print "immagine:", foto
    print "console:", console

    return {'nome':titolo, 'anno':anno, 'immagine':foto,'console':console,'upc':upc}