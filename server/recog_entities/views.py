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
    g = rdflib.Graph()
    # lee el archivo rdf
    g.parse("arroz_verde.rdf")
    # g.parse("ontology_arrozverde.rdf")
    prueba = "El caso 'receta de arroz verde 502' es una investigación publicada por el portal digital Mil Hojas. El portal digital reveló un correo electrónico recibido por Pamela Martínez —supuesta asesora del expresidente Rafael Correa según Mil Hojas— con un documento titulado ‘receta de arroz verde 502’.  Según la investigación, el remitente del correo electrónico sería Geraldo Luiz Pereira de Souza- encargado de la administración y finanzas de Odebrecht en Ecuador. El mail demuestra presuntos aportes entregados por empresas multinacionales —como Odebrecht— al movimiento Alianza País desde noviembre de 2013 a febrero de 2014—periodo en el que el expresidente Rafael Correa lideraba esa organización política. Según Mil Hojas, las donaciones alcanzarían los 11,6 millones de dólares. Las empresas que habrían realizado los aportes son: Constructora Norberto Odebrecht, SK Engineering & Construction, Sinohydro Corporation, Grupo Azul, Telconet, China International Water & Electric Corp-CWE."
    prIN("Texto de prueba\n", prueba)
    texto = ""
    mis_entidades = ""
    consulta = ""
    nlp = es_core_news_sm.load()
    if request.method == "POST" and 'buscar' in request.POST:
        # print("-->" + request.POST["palabraClave"])
        texto = request.POST["palabraClave"]
        texto = texto.replace("-", "")
        texto = texto.replace("—", "")
        texto = texto.replace("_", "")
        texto = texto.replace("á", "a")
        texto = texto.replace("é", "e")
        texto = texto.replace("í", "i")
        texto = texto.replace("ó", "o")
        texto = texto.replace("ú", "u")

    text = nlp(texto)
    tokenized_sentences = [sentence.text for sentence in text.sents]
    # crea diccionario vacio
    datos = []
    # iteracion del rdf mediante consulta sparql
    # obtiene predicado y objeto de la uri de datos de empacipada
    # Consulta de varios filtros
    entidadSpacy = []
    etiquetaEtiquetada = []
    for sentence in tokenized_sentences:
        for entity in nlp(sentence).ents:
            entidadSpacy.append(entity.text)
    # Eliminando duplicados en las listas, sin perder el orden
    entidadSpacy = list(set(entidadSpacy))

    for sentence in entidadSpacy:
        for entity in nlp(sentence).ents:
            etiquetaEtiquetada.append(entity.label_)
            # prGris(entity.label_)

    for entidadEncontrada in entidadSpacy:
        busca = entidadEncontrada  # -Entidad 1 Etiqueta
        # prGris(busca)
        consulta = 'PREFIX cavr: <http://data.utpl.edu.ec/arrozverde/resource/>\n'
        consulta = consulta + 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'
        consulta = consulta + 'SELECT DISTINCT ?s ?p ?o WHERE { { {?s ?p ?o .} FILTER (?p = cavr:type). } UNION { {?s ?p ?o .} OPTIONAL{?s cavr:nombre "%s"}. } UNION { {?s ?p ?o .} OPTIONAL{?s cavr:apellido "%s"}. } UNION { {?s ?p ?o .} OPTIONAL{?s cavr:nombreEmpresa "%s"}. } UNION { {?s ?p ?o .} OPTIONAL{?s cavr:nombrePais "%s"}. } UNION { {?s ?p ?o .} OPTIONAL{?s cavr:nombrePais "%s"}. } UNION { {?s ?p ?o .} FILTER(?p = cavr:codigoPersona). } UNION { {?s ?p ?o .} FILTER(?p = cavr:codigoEmpresa). } UNION { {?s ?p ?o .} FILTER(?p = cavr:codigoPais). } UNION { {?s ?p ?o .} OPTIONAL{?s cavr:liderImplicado "%s"}. } UNION { {?s ?p ?o. } OPTIONAL{?s cavr:involucrada "%s"}. } UNION { {?s ?p ?o. } OPTIONAL{?s rdfs:label "%s"}. } UNION { {?s ?p ?o. } OPTIONAL{?s rdfs:comment "%s"}. } }' % (busca, busca, busca, busca, busca, busca, busca, busca, busca)
        # prVerde(consulta)
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
            tripleta.append({"valor": sujeto, "url": sujeto})
            tripleta.append({"valor": predicado, "url": predicado})
            tripleta.append({"valor": objeto, "url": objeto})
            datos.append(tripleta)
    prAzul(consulta)
    # print(datos)
    ''' 
    str = "Messi is the best soccer player"
    "soccer" in str
     '''
    mis_entidades = texto
    prVerde(len(entidadSpacy))
    prVerde(len(etiquetaEtiquetada))

    # for entidadEncontrada in entidadSpacy:
    #     prCyan(entidadEncontrada)
    # for entidadEncontrada in etiquetaEtiquetada:
    #     prGris(entidadEncontrada)

    for entidadEncontrada in entidadSpacy:
        indice = entidadSpacy.index(entidadEncontrada)
        # prNegro(indice)
        if indice == len(entidadSpacy)-1:
            break
        else:
            etiqueta = etiquetaEtiquetada[indice]
        # prUnder(entidadEncontrada)
        # prIN(entidadEncontrada, etiqueta)
        entidadEtiquetada = entidadEncontrada + " (" + etiqueta + ")"
        mis_entidades = mis_entidades.replace(
            entidadEncontrada, entidadEtiquetada)
    # prAzul(mis_entidades)
    context = {
        'my_title': my_title,
        'texto': texto,
        'mis_entidades': mis_entidades,
        'datos': datos
    }

    return render(request, "index.html", context)


def info(request):
    return render(request, "info.html", {"title": "¿Como se trabajo?"})


def identificador(request):
    g = rdflib.Graph()
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


def prAzul(skk):
    print("\033[94m {}\033[00m" .format(skk))


def prUnder(skk):
    print("\033[4m {}\033[00m" .format(skk))


def prBold(skk):
    print("\033[1m {}\033[00m" .format(skk))


def prIN(a, b):
    print("\033[92m \033[94m %s \t\t %s" % (format(a), format(b)))
