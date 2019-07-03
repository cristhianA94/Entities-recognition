# Create your views here
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.http import Http404

from django.http import JsonResponse
import rdflib
from rdflib.serializer import Serializer

def loadindex(request):
    my_title = "Caso Arroz Verde"
    g=rdflib.Graph()
    # lee el archivo rdf
    g.parse("arroz_verde.rdf")
    keyword = ""
    # crea diccionario vacio
    datos = []
    # iteracion del rdf mediante consulta sparql
    # obtiene predicado y objeto de la uri de datos de empacipada
    # Consulta de varios filtros
    consulta = 'SELECT ?s ?p ?o  WHERE { ?s ?p ?o .FILTER regex(str(?s), "arrozverde") .}'
    for row in g.query(consulta):
        tripleta = []
        # agrega datos a diccionario
        sujeto = row.s.split("/")
        sujeto = sujeto[len(sujeto)-1]
        
        predicado = row.p.split("/")
        predicado = predicado[len(predicado)-1]
        
        objeto = row.o.split("/")
        objeto = objeto[len(objeto)-1]
        
        tripleta.append(sujeto)
        tripleta.append(predicado)
        tripleta.append(objeto)
        # print(tripleta)
        # print(*tripleta, sep = ", ")
        datos.append(tripleta)
    print(datos)

    if request.method == "POST" and 'buscar' in request.POST:
        print("-->" + request.POST["palabraClave"])
        keyword = request.POST["palabraClave"]
    
    context = {"titulo": my_title, 'datos': datos, "palabra": keyword}
    # print("\033[91m {}\033[00m" .format(datos))
    return render(request, "index.html", context)

def info(request):
    return render(request, "info.html", {"title": "¿Como se trabajo?"})

def identificador(request):
    g=rdflib.Graph()
    # lee el archivo rdf
    g.parse("Emancipada_final.rdf")

    # crea diccionario vacio
    data = {}
    # iteracion del rdf mediante consulta sparql
    consulta = 'SELECT ?s ?p ?o  WHERE { ?s ?p ?o .FILTER regex(str(?s), "emancipada") .}'
    for row in g.query(consulta):
        # obtiene predicado y objeto de la uri de datos de empacipada
        # Consulta de varios filtros
        # agrega datos a diccionario
        data[row.p] = row.o
        # retorna json con los datos obtenidos del
    return JsonResponse(data)
