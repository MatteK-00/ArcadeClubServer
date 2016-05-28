from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from arcadeclub.models import Magazzino, Gioco
from arcadeclub.serializers import GiocoSerializer,MagazzinoSerializer,MagazzinoSerializerShort
from arcadeclub.views import JSONResponse
from rest_framework import serializers
from requestSito import __webSearch
from requestSitoNew import __webSearchNew
import json
import base64
import urllib
import time

from django.core.serializers import serialize

#def index(request):
#   return HttpResponse("Hello, world. You're at the search_upc index.")

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