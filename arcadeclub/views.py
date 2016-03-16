from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from arcadeclub.models import Utente
from arcadeclub.serializers import UtenteSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)




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


#def utenti_detail(request):
#	return HttpResponse(status=204)

