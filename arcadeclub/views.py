from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from arcadeclub.models import Utente, Magazzino, Venduti, Gioco
from arcadeclub.serializers import UtenteSerializer, MagazzinoSerializer, VendutiSerializer, GiocoSerializer, MagazzinoSerializerShort
from requestSitoNew import __webSearchNew
import base64
import urllib
import time
import json

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



def controlla_token(id_telefono):
    n_result = Utente.objects.filter(device=id_telefono).count()
    if (n_result > 0):
        return True
    else:
        return False


@csrf_exempt
def image(request,id_telefono,image_file):
    if request.method == 'GET':
        if (controlla_token(id_telefono)):
            if "_" not in image_file:
                print "sono qui: "+ image_file
                gioco = Gioco.objects.get(upc=image_file)
                image_file = str(gioco.id_gioco) + "_" + str(gioco.immagine)

            in_file = open("image/"+image_file,"r")
            encoded_image = in_file.read()
            in_file.close()
            return HttpResponse(encoded_image,status=200)
        else:
            return HttpResponse(status=401)

@csrf_exempt
def utenti_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        utenti = Utente.objects.all()
        serializer = UtenteSerializer(utenti, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UtenteSerializer(data=data)
        #if serializer.is_valid():
        serializer.save()
        return JSONResponse(serializer.data, status=201)
    return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def utenti_detail(request, id):
    """
    Retrieve, update or delete a code utente.
    """
    try:
        utente = Utente.objects.get(id=id)
    except Utente.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UtenteSerializer(utente)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UtenteSerializer(utente, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        utente.delete()
        return HttpResponse(status=204)

@csrf_exempt
def utenti_loginRequest(request, username, pwd):
    """
    Retrieve, update or delete a code utente.
    """
    try:
        utente = Utente.objects.get(username=username,pwd=pwd)
    except Utente.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        return JSONResponse(utente.device)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UtenteSerializer(utente, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        utente.delete()
        return HttpResponse(status=204)


def magazzino_detail(request,id_telefono):
    print id_telefono
    if (controlla_token(id_telefono)):
        if request.method == 'GET':
            print "SONO LA RICHIESTA! "
            #id_item = request.GET.get("id_item",'')
            upc  = request.GET.get("upc",'')
            nome = request.GET.get("nome",'')
            anno = request.GET.get("anno",'')
            console = request.GET.get("console",'')
            stato = request.GET.get("stato",'')
            quality = request.GET.get("quality",'')
            #prezzo_acquisto = request.GET.get("prezzo_acquisto",'')
            #data_acquisto = request.GET.get("data_acquisto",'')
            #note = request.GET.get("note",'') la ricerca per campi null e' un problema al momento

            sold = request.GET.get("sold",'false')

            print request.GET
            
            #magazzino = Magazzino.objects.filter(id_item__contains=id_item, upc__contains=upc, nome__contains=nome, anno__contains=anno,
            #    console__contains=console, stato__contains=stato, quality__contains=quality, prezzo_acquisto__contains=prezzo_acquisto,
            #    data_acquisto__contains=data_acquisto)

            magazzino = Magazzino.objects.filter(upc__contains=upc, nome__contains=nome, anno__contains=anno,
                console__contains=console, stato__contains=stato, quality__contains=quality)   #prezzo_vendita__isnull=False

            venduti = [];
            if (sold == "true"):
                venduti = Venduti.objects.filter(upc__contains=upc, nome__contains=nome, anno__contains=anno,
                    console__contains=console, stato__contains=stato, quality__contains=quality)


            magazzinoSerializzato = MagazzinoSerializer(magazzino,many=True)
            vendutiSerializzato = VendutiSerializer(venduti,many=True)

            risposta = {}
            risposta['in_magazzino'] = magazzinoSerializzato.data
            risposta['venduti'] = vendutiSerializzato.data
            json_data = json.dumps(risposta)
            return HttpResponse(json_data)

        if request.method == 'POST':
            print "put al db"
            upc  = request.POST.get("upc",'')
            nome = request.POST.get("nome",'')
            anno = request.POST.get("anno",'')
            console = request.POST.get("console",'')
            stato = request.POST.get("stato",'')
            quality = request.POST.get("quality",'')
            prezzo_acquisto = request.POST.get("prezzo_acquisto",'')
            data_acquisto = request.POST.get("data_acquisto",'')
            note = request.POST.get("note",'')

            item_nuovo = Magazzino(upc=upc, nome=nome,anno=anno,console=console,stato=stato,quality=quality,
                data_acquisto=data_acquisto,prezzo_acquisto=prezzo_acquisto,note=note)
            item_nuovo.save()    #SALVA NEL DB SE PRIMA NON ERA PRESENTE - IMPORTANTE!
            return HttpResponse(status=200)
    else:
        return HttpResponse(status=401)



def venduti_detail(request,id_telefono):
    if (controlla_token(id_telefono)):
        if request.method == 'POST':
            print "vendo oggetto"
            id_item  = request.POST.get('id_item','ERROR')
            prezzo  = request.POST.get('prezzo','')
            data  = request.POST.get('data','')

            if id_item != "ERROR":
                try: 
                    item_venduto = Magazzino.objects.get(id_item=id_item)

                    venduto = Venduti(upc=item_venduto.upc,nome=item_venduto.nome,anno=item_venduto.anno,
                    console=item_venduto.console,stato=item_venduto.stato,quality=item_venduto.quality,
                    prezzo_acquisto=item_venduto.prezzo_acquisto,data_acquisto=item_venduto.data_acquisto,
                    prezzo_vendita=prezzo,data_vendita=data,note=item_venduto.note)
                    
                    venduto.save()
                    item_venduto.delete()
                    return HttpResponse(status=200)
                
                except Magazzino.DoesNotExist:
                    return HttpResponse(status=404)
            return HttpResponse(status=204)
    else:
        return HttpResponse(status=401)


@csrf_exempt
def searchUpcRequest(request,id_telefono,upc):
    """
    Retrieve, update or delete a code gioco e magazzino.
    """
    if (controlla_token(id_telefono)):
        try:
            gioco = Gioco.objects.get(upc=upc)
        except Gioco.DoesNotExist:
            #datiGioco = __webSearch(upc)
            datiGioco = __webSearchNew(upc)
            if (datiGioco['nome']==''):
                return HttpResponse(status=404)

            resource = urllib.urlopen(datiGioco['immagine'])
            encoded_string = base64.b64encode(resource.read())
            timestamp = str(time.time()).replace(".","")
            
            gioco_nuovo = Gioco(upc=datiGioco['upc'], nome=datiGioco['nome'],anno=datiGioco['anno'],console=datiGioco['console'],immagine=timestamp)
            
            gioco_nuovo.save()    #SALVA NEL DB SE PRIMA NON ERA PRESENTE - IMPORTANTE!
            gioco = Gioco.objects.get(upc=upc)
            id_gioco = gioco.id_gioco

            out_file = open("image/"+str(id_gioco) +"_"+timestamp,"w")
            out_file.write(encoded_string)
            out_file.close()

            gioco_serializer = GiocoSerializer(gioco_nuovo, many=False)
            risposta = {}
            risposta['info'] = gioco_serializer.data
            #risposta['item_list']
            json_data = json.dumps(risposta)
            return HttpResponse(json_data)
        if request.method == 'GET':
            #giochi = Magazzino.objects.filter(upc=upc)
            # serializedList = serialize('json', list(giochi), fields=('id_item','console','stato','prezzo_acquisto','upc','nome','quality','data_acquisto','note'))
            # serializer = GiocoSerializer(gioco, many=False)
            # json = JSONRenderer().render(serializer.data)
            # return HttpResponse([json,serializedList])
            #ids = Entry.objects.values_list('stato','quality','prezzo_acquisto','data_acquisto','note', flat=True).filter(upc=upc)
            #my_models = MyModel.objects.filter(pk__in=set(ids))
            giochi = Magazzino.objects.filter(upc=upc).values('id_item','stato','quality','prezzo_acquisto','data_acquisto','note').distinct()
            #giochi = Magazzino.objects.filter(upc=upc)
            serializedList = MagazzinoSerializerShort(giochi, many=True)
            gioco_serializer = GiocoSerializer(gioco, many=False)
            #jsonList = JSONRenderer().render(serializedList.data)
            #jsonGioco = JSONRenderer().render(serializer.data)
            risposta = {}
            risposta['info'] = gioco_serializer.data
            risposta['item_list'] = serializedList.data
            json_data = json.dumps(risposta)
            return HttpResponse(json_data)

            #return HttpResponse([jsonGioco,jsonList])

        elif request.method == 'PUT':
            data = JSONParser().parse(request)
            serializer = UtenteSerializer(utente, data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data)
            return JSONResponse(serializer.errors, status=400)

        elif request.method == 'DELETE':
            utente.delete()
            return HttpResponse(status=204)
    else:
        return HttpResponse(status=401)