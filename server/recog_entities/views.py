# Create your views here
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from rdflib.serializer import Serializer
from collections import OrderedDict
from SPARQLWrapper import SPARQLWrapper, JSON
# spacy
import spacy
import es_core_news_sm


def loadindex(request):
    # Carga lenguaje español Spacy
    nlp = es_core_news_sm.load()

    my_title = "Caso Arroz Verde"
    texto = ""
    prueba = "El caso Arroz Verde es una investigación publicada por el portal digital Mil Hojas. El portal digital reveló un correo electrónico recibido por Pamela Martínez supuesta asesora del expresidente Rafael Correa según Mil Hoja con un documento titulado Receta de Arroz Verde 502.  Según la investigación, el remitente del correo electrónico sería Geraldo Luiz Pereira de Souza, encargado de la administración y finanzas de Odebrecht en Ecuador. El mail demuestra presuntos aportes entregados por empresas multinacionales como Odebrecht al movimiento Alianza País desde noviembre de 2013 a febrero de 201 periodo en el que el expresidente Rafael Correa lideraba esa organización política. Según, Mil Hojas, las donaciones alcanzarían los 11,6 millones de dólares. Las empresas que habrían realizado los aportes son: Constructora Norberto Odebrecht, SK Engineering & Construction, Sinohydro Corporation, Grupo Azul, Telconet, China International Water & Electric Corp-CWE."
    datos = []

    # Endpoint con Virtuoso
    sbcEndpoint = SPARQLWrapper("http://localhost:8890/sparql/")
    # Se carga el texto de prueba
    if request.method == "POST" and 'prueba' in request.POST:
        texto = prueba
    # Obtiene el texto de entrada
    if request.method == "POST" and 'buscar' in request.POST:
        texto = request.POST["palabraClave"]

    texto = limpiarDatos(texto)
    text = nlp(texto)
    # Tokeniza la entrada de texto con Spacy
    tokenized_sentences = [sentence.text for sentence in text.sents]

    entidadSpacy = []
    # Reconocimiento de entidades con Spacy
    for sentence in tokenized_sentences:
        for entity in nlp(sentence).ents:
            entidadSpacy.append(entity.text)
    # Eliminando duplicados en las listas, sin perder el orden
    entidadSpacy = list(set(entidadSpacy))

    etiquetaEntidad = []
    # Etiqueta de las entidades
    for sentence in entidadSpacy:
        for entity in nlp(sentence).ents:
            prVerde(entity.text)
            etiquetaEntidad.append(entity.label_)

    palabras_limpias = []
    # Limpieza de datos de las entidades
    for enti in entidadSpacy:
        palabra = enti  # -Entidad 1 Etiqueta
        palabra = palabra.replace(' ', '_')
        palabra = palabra.replace('—', '')
        palabra = palabra.replace('á', 'a')
        palabra = palabra.replace('é', 'e')
        palabra = palabra.replace('í', 'i')
        palabra = palabra.replace('ó', 'o')
        palabra = palabra.replace('ú', 'u')
        palabras_limpias.append(palabra)

        """
        PREFIX cavr: <http://localhost:8080/negociador/page>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?s ?p ?o
        OPTIONAL{?s cavr:nombre "Pamela" ;
        FROM <http://localhost:8890/SBC>
        WHERE
        {
        ?s ?p ?o .
                    cavr:apellido "Pamela" ;
                    cavr:nombrePartido "Pamela" ;
                    cavr:nombreEmpresa "Pamela" ;
                    cavr:nombrePais "Pamela" ;
                    cavr:liderImplicado "Pamela" ;
                    cavr:involucrada "Pamela" ;
                    cavr:autoriza "Pamela" ;
                    cavr:nombradoPor "Pamela" .}
        OPTIONAL{?a rdf:rest ?o ;
                    rdf:first ?o ;
                    rdfs:subPropertyOf ?o ;
                    owl:members ?o ;
                    rdf:type owl:Class ;
                    rdf:type owl:Ontology ;
                    rdf:type owl:ObjectProperty ;
                    rdf:type owl:DatatypeProperty ;
                    rdf:type owl:AsymmetricProperty ;
                    rdf:type owl:AllDisjointClasses ;
                    rdf:type owl:AllDisjointProperties .}
        OPTIONAL{?s rdfs:label "Pamela" .}
        OPTIONAL{?s rdfs:comment "Pamela" .}
        }
        """
        # Consulta SPARQL para buscar en la BD la entidad encontrada
        consulta = """
            SELECT ?s ?p ?o
            FROM <http://localhost:8890/SBC>
            WHERE 
            { 
                ?s ?p ?o .FILTER (regex(str(?s), "%s") || regex(str(?o), "%s")) .
            }
            """ % (palabra, palabra)
        print("Palabra: ", palabra)
        # prGris(busca)
        # Ejecuta la consulta en el Endpoint de Virtuoso
        sbcEndpoint.setQuery(consulta)
        # Retorna en datos JSON
        sbcEndpoint.setReturnFormat(JSON)
        results = sbcEndpoint.query().convert()
        print(results)
        # Dentro del JSON en el atriibuto "results" con el atributo "bindings"
        # Lectura de JSON y division en tripletas
        for result in results["results"]["bindings"]:
            lista = []
            listaS = result["s"]["value"]
            listaP = result["p"]["value"]
            listaO = result["o"]["value"]
            lista.append(listaS)
            lista.append(listaP)
            lista.append(listaO)
            datos.append(lista)
    # Elimina tripletas duplicadas
    datos = OrderedDict((tuple(x), x) for x in datos).values()

    print(len(entidadSpacy))
    print(len(etiquetaEntidad))
    # prVerde(len(entidadSpacy))
    # prVerde(len(etiquetaEntidad))
    # Valor del texto de entrada
    mis_entidades = texto

    print("---------------------------------")
    print(palabras_limpias)

    # Imprimir texto con etiquetas de entidades de Spacy
    for enti in palabras_limpias:
        # Saca el indice de cada palabra del arreglo
        indice = palabras_limpias.index(enti)
        if indice == len(palabras_limpias):
            break
        else:
            entidadEtiquetada = '<a class="btn btn-success btn-sm" href="http://localhost:8080/negociador/page/' + \
                enti + '" role="button">'+entidadSpacy[indice]+"</a>"
        # prUnder(entidadEncontrada)
        # prIN(entidadEncontrada, etiqueta)
        mis_entidades = mis_entidades.replace(
            entidadSpacy[indice], entidadEtiquetada)

    prAzul(datos)
    # Diccionario visualizacion en template
    context = {
        'my_title': my_title,
        'texto': texto,
        'mis_entidades': mis_entidades,
        'datos': datos
    }
    return render(request, "index.html", context)


def info(request):
    return render(request, "info.html", {"title": "¿Como se trabajo?"})


def page_not_found(request):
    # Dict to pass to template, data could come from DB query
    mensaje = "No se pudo localizar el recurso buscado compruebe la ruta una vez, en caso de estar en lo correcto; corregiremos el inconveniente."
    values_for_template = {"error": mensaje}
    return render(request, '404.html', values_for_template, status=404)


def limpiarDatos(palabra):
    palabra = str(palabra)
    # print('***'*10)
    # print(palabra)
    # palabra = palabra.replace("-", "")
    palabra = palabra.replace('—', '')
    palabra = palabra.replace('á', 'a')
    palabra = palabra.replace('é', 'e')
    palabra = palabra.replace('í', 'i')
    palabra = palabra.replace('ó', 'o')
    palabra = palabra.replace('ú', 'u')
    # print(palabra)
    # print('***'*10)
    return palabra


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
