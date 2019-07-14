# Create your views here
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
import rdflib
from rdflib.serializer import Serializer
# spacy
import spacy
import es_core_news_sm


def loadindex(request):
    my_title = "Caso Arroz Verde"
    g=rdflib.Graph()
    # lee el archivo rdf
    g.parse("arroz_verde.rdf")
    texto = ""
    mis_entidades = ""

    if request.method == "POST" and 'buscar' in request.POST:
        # print("-->" + request.POST["palabraClave"])
        texto = request.POST["palabraClave"]
    nlp = es_core_news_sm.load()
    text = nlp(texto)
    tokenized_sentences = [sentence.text for sentence in text.sents]
    # print(tokenized_sentences)
    # crea diccionario vacio
    datos = []
    # iteracion del rdf mediante consulta sparql
    # obtiene predicado y objeto de la uri de datos de empacipada
    # Consulta de varios filtros
    entidadSpacy = []
    for sentence in tokenized_sentences:
        entidadEncontrada = []
        for entity in nlp(sentence).ents:
            entidadEncontrada.append(entity.text)
            entidadEncontrada.append(entity.label_)
            entidadSpacy.append(entidadEncontrada)
            busca = "resource/" # entity.text
            consulta = 'SELECT ?s ?p ?o  WHERE { ?s ?p ?o .FILTER regex(str(?p), "%s") .}' % (busca)
            for row in g.query(consulta):
                tripleta = []
                # sujeto = row.s.split("/")
                # predicado = row.p.split("/")
                # objeto = row.o.split("/")
                # sujeto = sujeto[len(sujeto)-1]
                # predicado = predicado[len(predicado)-1]
                # objeto = objeto[len(objeto)-1]
                sujeto = row.s
                predicado = row.p
                objeto = row.o
                
                sujeto = sujeto.replace('http://data.utpl.edu.ec/arrozverde/', 'http://localhost:8080/negociador/')
                predicado = predicado.replace('http://data.utpl.edu.ec/arrozverde/', 'http://localhost:8080/negociador/')
                objeto = objeto.replace('http://data.utpl.edu.ec/arrozverde/', 'http://localhost:8080/negociador/')
                urlS = sujeto.replace('http://data.utpl.edu.ec/arrozverde/resource/', 'http://192.168.1.12:8080/negociador/page/')
                urlP = predicado.replace('http://data.utpl.edu.ec/arrozverde/resource/', 'http://192.168.1.12:8080/negociador/page/')
                urlO = objeto.replace('http://data.utpl.edu.ec/arrozverde/resource/', 'http://192.168.1.12:8080/negociador/page/')
                # tripleta.append(sujeto)
                # tripleta.append(objeto)
                tripleta.append({"valor": sujeto, "url": urlS})
                tripleta.append({"valor": predicado, "url": urlP})
                tripleta.append({"valor": objeto, "url": urlO})
                datos.append(tripleta)

                sujeto = row.s.split("/")
                sujeto = sujeto[len(sujeto)-1]
    # print(datos)
    ''' 
    str = "Messi is the best soccer player"
    "soccer" in str
     '''
    mis_entidades = texto
    for entidadEncontrada in entidadSpacy:
        # print (entidadEncontrada)
        entidadEncontrada[0] = entidadEncontrada[0].replace("_", " ")
        entidadEtiquetada = entidadEncontrada[0] + "(" + entidadEncontrada[1] + ")"
        # print("entidadEtiquetada", entidadEtiquetada)
        mis_entidades = mis_entidades.replace(entidadEncontrada[0], entidadEtiquetada)
    prVerde(mis_entidades)
    context = {'my_title': my_title,
    'texto': texto,
    'mis_entidades': mis_entidades,
    'datos': datos}
    prCyan(mis_entidades)
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
    consulta = 'SELECT ?s ?p ?o  WHERE { ?s ?p ?o .FILTER regex(str(?s), "resource") .}'
    for row in g.query(consulta):
        # obtiene predicado y objeto de la uri de datos de empacipada
        # Consulta de varios filtros
        # agrega datos a diccionario
        data[row.p] = row.o
        # retorna json con los datos obtenidos del
    return JsonResponse(data)


@csrf_exempt
def buscapalabra_ajax(request):
    keyword = ""
    context = {}
    if request.is_ajax() == True:
        # keyword = request.POST.getlist('valor')[0]
        # print("-->AJAX\n" + request.POST.get('valor')
        keyword = request.POST.getlist('valor', False)
        print("-->AJAX\n", keyword)
    context = {"texto": keyword, "mensaje": "Mensaje de salida"}
    return JsonResponse(context, safe=False)


def prCyan(skk):
    print("\033[96m {}\033[00m" .format(skk))
def prGris(skk):
    print("\033[97m {}\033[00m" .format(skk))
def prNegro(skk):
    print("\033[98m {}\033[00m" .format(skk))
def prVerde(skk):
    print("\033[92m {}\033[00m" .format(skk))
