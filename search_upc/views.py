from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from arcadeclub.models import Magazzino, Gioco
from arcadeclub.serializers import GiocoSerializer,MagazzinoSerializer
from arcadeclub.views import JSONResponse
from rest_framework import serializers
from requestSito import __webSearch
import json

from django.core.serializers import serialize

#def index(request):
#   return HttpResponse("Hello, world. You're at the search_upc index.")

@csrf_exempt
def searchUpcRequest(request, upc):
    """
    Retrieve, update or delete a code gioco e magazzino.
    """
    try:
        gioco = Gioco.objects.get(upc=upc)
    except Gioco.DoesNotExist:
        datiGioco = __webSearch(upc)
        if (datiGioco['nome']==None):
            return HttpResponse(status=404)
        gioco_nuovo = Gioco(upc=datiGioco['upc'], nome=datiGioco['nome'],anno=datiGioco['anno'],console=datiGioco['console'],immagine=datiGioco['immagine'])
        #gioco_nuovo.save()
        #jsonarray = json.dumps(datiGioco)
        serializer = GiocoSerializer(gioco_nuovo, many=False)
        return JSONResponse(serializer.data)#, status=201)

    if request.method == 'GET':
        giochi = Magazzino.objects.filter(upc=upc)
        # serializedList = serialize('json', list(giochi), fields=('id_item','console','stato','prezzo_acquisto','upc','nome','quality','data_acquisto','note'))
        # serializer = GiocoSerializer(gioco, many=False)
        # json = JSONRenderer().render(serializer.data)
        # return HttpResponse([json,serializedList])
        giochi = Magazzino.objects.filter(upc=upc)
        serializedList = MagazzinoSerializer(giochi, many=True)
        serializer = GiocoSerializer(gioco, many=False)
        jsonList = JSONRenderer().render(serializedList.data)
        json = JSONRenderer().render(serializer.data)
        return HttpResponse([json,jsonList])

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
 