import urllib2
import ssl
from functools import wraps
def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar

ssl.wrap_socket = sslwrap(ssl.wrap_socket)

# upc = "008888322177"  # <-> 187 Ride or Die (ps2)
# upc = "720238101804"  # <-> Exile (Sega Genesis)
#upc = "045496730352"  # <-> donkey kong (gameboy)

def __webSearch(upc):

    ssl.wrap_socket = sslwrap(ssl.wrap_socket)


    sito = "http://videogames.pricecharting.com/search?q=" + upc

    titolo = ""
    anno = ""
    foto = ""
    console = ""

    if True:
        user_agent = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3"
        headers = {"User-Agent": user_agent}

        try:
            req = urllib2.Request(sito, None, headers)
            try:
                response = urllib2.urlopen(req)
                page = response.read()
                #print page
                temp = page
                temp = temp.split("Prices")

                titolo = temp[0].split("<title>")[1]

                console = temp[1].split(" | Compare Loose")[0]

                console = console.replace("(", "").replace(")", "").replace(" ", "")

                anno = (page.split("class=\"date\">")[1]).split("<")[0]

                foto = page.split("<img src=\"")[1].split("\"")[0]

            except urllib2.HTTPError, err:
                if err.code == 404:
                    print "CodiceErrore err.code == 404"
                    return {"CodiceErrore":"err.code == 404"}
                else:
                    print "CodiceErrore err.code ==" + err.code
                    return  {"CodiceErrore":"else"}
        except Exception, e:
            print e
            pass

    print "nome:", titolo
    print "anno:", anno
    print "immagine:", foto
    print "console:", console

    return {'nome':titolo, 'anno':anno, 'immagine':foto,'console':console,'upc':upc}