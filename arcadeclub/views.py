from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from arcadeclub.models import Utente, Magazzino, Venduti
from arcadeclub.serializers import UtenteSerializer, MagazzinoSerializer, VendutiSerializer
import json

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



@csrf_exempt
def image(request,image_file):
    if request.method == 'GET':
        in_file = open("image/"+image_file,"r")
        encoded_image = in_file.read()
        in_file.close()
        return HttpResponse(encoded_image)

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


def magazzino_detail(request):
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

    if reguest.method == 'PUT':
        print "put al db"
        upc  = request.PUT.get("upc",'')
        nome = request.PUT.get("nome",'')
        anno = request.PUT.get("anno",'')
        console = request.PUT.get("console",'')
        stato = request.PUT.get("stato",'')
        quality = request.PUT.get("quality",'')
        prezzo_acquisto = request.PUT.get("prezzo_acquisto",'')
        data_acquisto = request.PUT.get("data_acquisto",'')
        note = request.PUT.get("note",'')

        item_nuovo = Magazzino(upc=upc, nome=nome,anno=anno,console=console,stato=stato,quality=quality,
            prezzo_acquisto=prezzo_acquisto,data_acquisto=data_acquisto,note=note)
        item_nuovo.save()    #SALVA NEL DB SE PRIMA NON ERA PRESENTE - IMPORTANTE!
        return HttpResponse(status=200)



def venduti_detail(request):
    if request.method == 'POST':
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

