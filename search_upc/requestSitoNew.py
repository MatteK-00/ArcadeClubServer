import urllib3
import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

def __webSearchNew(upc):

    sito = "http://videogames.pricecharting.com/search?q=" + upc

    s = requests.Session()
    s.mount('http://', MyAdapter())
    r = s.get(sito)
	# You're ready to make verified HTTPS requests.
    try:
        print r.text
    except urllib3.exceptions.SSLError as e:
        print e