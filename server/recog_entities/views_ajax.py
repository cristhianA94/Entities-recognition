from django.shortcuts import render
from django.shortcuts import render, render_to_response, RequestContext
from camasweb.models import *
from django.http import HttpResponse
from django.utils.encoding import smart_unicode,smart_str
import json

def index(request):
    return render_to_response('index.html',
    context=RequestContext(request))

def graficas(request):
    objProvincia = Provincia.objects.filter()
    ctx = {'provincia':objProvincia}
    return render(render,'graficas.html',ctx,
    context_instance=RequestContext(request))

def datosCamasPorProvincia(request):
    objNombresProvincias = Provincia.objects.filter()
    ctx = {'nombreProvincias':objNombresProvincia}

    return render(render,'contactos.html',ctx,
    context_instance=RequestContext(request))

def graficas(request):
    objProvincia = Provincia.objects.filter()
    ctx = {'provincia':objProvincia}
    return render(render,'graficas.html',ctx,
    context_instance=RequestContext(request))



def graficarProvincias(request):
    objProvincia = Provincia.objects.filter()
    ctx = {'provincia':objProvincia}

    if request.method == 'POST':
        sProvincia = request.POST['selecccionarProvincia']
        idprovincia = Provincia.objects.get(idprovincia=sProvincia)

        numCantones = Canton.objects.filter(provincia_idprovincia = idprovincia).count()
        listCanton=[]
        listCanton.append(['Provincia','Cantones'])
        listCanton.append([smart_str(idprovincia.nombreprovincia),numCantones])
        ctx = {'provincia':objProvincia,'listaCanton':listCanton}

    return render(render,'graficas.html',ctx,
    context_instance=RequestContext(request))

def entidad(request):
    ctx=""
    cont = 0
    sumEstablecimeintos = 0
    listaEntidad = []
    listaEntidad.append(['Entidades', 'Numero establecimientos por entidad'])
    objEntidad = Entidad.objects.filter()
    for unaEntidad in objEntidad:
        establecimientos = Establecimiento.objects.filter( entidad_identidad = unaEntidad.pk)
        for unEstablecimiento in establecimientos:
            sumEstablecimeintos = sumEstablecimeintos + 1
        listaEntidad.append([str(unaEntidad.nombreentidad),sumEstablecimeintos])
        sumEstablecimeintos = 0

    ctx={'listaEntidad':listaEntidad}
    return render(render,'entidad.html',ctx,
    context_instance=RequestContext(request))

def clase(request):
    ctx=""
    cont = 0
    sumEstablecimeintos = 0
    listaClases = []
    listaClases.append(['Clases', 'Numero establecimientos por clase'])
    objClase = Clase.objects.filter()
    for unaClase in objClase:
        establecimientos = Establecimiento.objects.filter(clase_idclase = unaClase.pk)
        for unaEstablecimiento in establecimientos:
            sumEstablecimeintos = sumEstablecimeintos + 1
        listaClases.append([str(unaClase.nombreclase),sumEstablecimeintos])
        sumEstablecimeintos = 0

    ctx={'listaClases':listaClases}
    return render(render,'clase.html',ctx,
    context_instance=RequestContext(request))

def tipo(request):
    ctx=""
    cont = 0
    sumEstablecimeintos = 0
    listaTipo= []
    listaTipo.append(['Tipos', 'Numero establecimientos por Tipo'])
    objTipo = Tipo.objects.filter()
    for unTipo in objTipo:
        establecimientos = Establecimiento.objects.filter(tipo_idtipo = unTipo.pk)
        for unaEstablecimiento in establecimientos:
            sumEstablecimeintos = sumEstablecimeintos + 1
        listaTipo.append([str(unTipo.nombretipo),sumEstablecimeintos])
        sumEstablecimeintos = 0

    ctx={'listaTipo':listaTipo}
    return render(render,'tipo.html',ctx,
    context_instance=RequestContext(request))

def contactos(request):
    objNombreprovincia = Provincia.objects.filter()
    ctx = {'provincia':objNombreprovincia}
    if request.method == 'POST' and request.POST['seleccionarProvincia']:
        idprovincia = request.POST['seleccionarProvincia']
        provincia = Provincia.objects.get(idprovincia=idprovincia)
        cantones = Canton.objects.filter(provincia_idprovincia=provincia)
        ctx = {'provincia':objNombreprovincia,'nombreCantones':cantones,'idprovinciaselect':int(idprovincia)}
    return render(render,'contactos.html',ctx,
    context_instance=RequestContext(request))
def contactos2(request):
    objNombreprovincia = Provincia.objects.filter()
    if  request.POST['seleccionarCanton']:
        valortxt = request.POST['valor']
        cantones = Canton.objects.filter(provincia_idprovincia=valortxt)
        idcanton = request.POST['seleccionarCanton']
        canton = Canton.objects.get(idcanton=idcanton)
        parroquias = Parroquia.objects.filter(canton_idcanton=canton)
        ctx = {'provincia':objNombreprovincia,'nombreparroquia':parroquias,'canton':int(idcanton),'nombreCantones':cantones,'idprovinciaselect':int(valortxt)}
    return render(render,'contactos.html',ctx,
    context_instance=RequestContext(request))
def listar_establecimientos(request):
    objNombreprovincia = Provincia.objects.filter()
    if  request.POST['seleccionarParroquia']:
        idparroquia = request.POST['seleccionarParroquia']
        idcanton=request.POST['valor2']
        valortxt = request.POST['valor']
        parroquias = Parroquia.objects.filter()
        idparroq = Parroquia.objects.get(idparroquia=idparroquia)
        cantones = Canton.objects.filter(provincia_idprovincia=valortxt)
        establecimiento = Establecimiento.objects.filter(parroquia_idparroquia=idparroq)
        ctx = {'parroquiasid':int(idparroquia),'provincia':objNombreprovincia,'nombreparroquia':parroquias,'establecimientos':establecimiento,'canton':int(idcanton),'nombreCantones':cantones,'idprovinciaselect':int(valortxt)}
    return render(render,'contactos.html',ctx,
    context_instance=RequestContext(request))

def mapa(request):
    lugar=Hospital.objects.all()
    return render(request,'mapa.html',{'lugar':lugar})




def acercade(request):
    return render_to_response('acercade.html',
    context=RequestContext(request))

def informacion(request):
    return render_to_response('informacion.html',
    context=RequestContext(request))

def quienessomos(request):
    ctx = ""
    lista_cantones = []
    objProvincia = Provincia.objects.filter(idprovincia = 11)


    ctx = {'nombreP':objProvincia}
    return render(render,'quienessomos.html',ctx,
    context_instance=RequestContext(request))

def master(request):
    return render_to_response('master.html',
    context=RequestContext(request))

def camasparroquia(request):
    return render_to_response('camasparroquia.html',
    context=RequestContext(request))

def camas_por_provincia(request):
    hospitalesPorProvincia = []
    noVacio = 0
    objProvincia = Provincia.objects.all()
    ctx = {'provincia':objProvincia}
    if request.method == 'POST':
        sProvincia = request.POST['seleccionarProvincia']
        idProvincia = Provincia.objects.get(idprovincia=sProvincia)
        idCanton = Canton.objects.filter(provincia_idprovincia__idprovincia = idProvincia.idprovincia)
        for ctn in idCanton:
            hospitales = Hospital.objects.filter(canton_idcanton__idcanton = ctn.idcanton)
            noVacio = len(hospitales)
            if noVacio>0:
                for h in hospitales:
                    hospitalesPorProvincia.append(h)
        ctx = {'provincia':objProvincia,'canton':idCanton,'hospitales':hospitalesPorProvincia,'idprovinciaselect':int(sProvincia)}

    return render(render,'camas_por_provincia.html',ctx,
    context_instance=RequestContext(request))
def cobertura(request):
    objAnios = Anios.objects.filter()
    ctx = {'allAnios':objAnios}
    if request.method == 'POST':
         anios = request.POST.get('selecccionarAnio')
         var = request.POST.get('selecccionarVariable')
         datosAnio = int(anios)
         traerAnios = Anio.objects.filter(anio = datosAnio)
    ctx = {'allAnios':objAnios,'datoAnio':traerAnios}
    return render(render,'cobertura.html',ctx,
    context_instance=RequestContext(request))

def clase_establecimiento(request):
    ctx = ""
    soloAnio = 0
    lon = 0
    contEstablecimientos = 0
    listaEstablecimientos = []
    objAnios = Anios.objects.all()
    ctx = {'anios':objAnios}
    listaEstablecimientos.append(['Clase de establecimientos','Numero de establecimientos'])
    if request.method == 'POST':
        soloAnio = request.POST['selecccionarAnio']
        objClases = Clase.objects.all()
        for c in objClases:
            objEstablecimientos = Establecimiento.objects.filter(clase_idclase = c.idclase, anios_idanios = soloAnio)
            lon = len(objEstablecimientos)
            print lon
            if lon > 0:
                for est in objEstablecimientos:
                    contEstablecimientos = contEstablecimientos + 1
                listaEstablecimientos.append([str(c.nombreclase),contEstablecimientos])
                contEstablecimientos = 0
    ctx = {'anios':objAnios,'establecimientoPorClase':listaEstablecimientos,'idanioselect':int(soloAnio)}
    return render(render,'clase_establecimiento.html',ctx,
    context_instance=RequestContext(request))


def tipo_establecimiento(request):
    ctx = ""
    soloAnio = 0
    lon = 0
    contEstablecimientos = 0
    listaEstablecimientos = []
    objAnios = Anios.objects.all()
    ctx = {'anios':objAnios}
    listaEstablecimientos.append(['Establecimientos por entidad','Numero de establecimientos'])
    if request.method == 'POST':
        soloAnio = request.POST['selecccionarAnio']
        objTipos = Tipo.objects.all()
        for c in objTipos:
            objEstablecimientos = Establecimiento.objects.filter(tipo_idtipo = c.idtipo, anios_idanios = soloAnio)
            lon = len(objEstablecimientos)
            print lon
            if lon > 0:
                for est in objEstablecimientos:
                    contEstablecimientos = contEstablecimientos + 1
                listaEstablecimientos.append([str(c.nombretipo),contEstablecimientos])
                contEstablecimientos = 0
    ctx = {'anios':objAnios,'establecimientoPorTipo':listaEstablecimientos,'idanioselect':int(soloAnio)}
    return render(render,'tipo_establecimiento.html',ctx,
    context_instance=RequestContext(request))
def entidad_establecimiento(request):
    ctx = ""
    soloAnio = 0
    lon = 0
    contEstablecimientos = 0
    listaEstablecimientos = []
    objAnios = Anios.objects.all()
    ctx = {'anios':objAnios}
    listaEstablecimientos.append(['Establecimientos por entidad','Numero de establecimientos'])
    if request.method == 'POST':
        soloAnio = request.POST['selecccionarAnio']
        objEntidad = Entidad.objects.all()
        for c in objEntidad:
            objEstablecimientos = Establecimiento.objects.filter(entidad_identidad = c.identidad, anios_idanios = soloAnio)
            lon = len(objEstablecimientos)
            print lon
            if lon > 0:
                for est in objEstablecimientos:
                    contEstablecimientos = contEstablecimientos + 1
                listaEstablecimientos.append([str(c.nombreentidad),contEstablecimientos])
                contEstablecimientos = 0
    ctx = {'anios':objAnios,'establecimientoPorEntidad':listaEstablecimientos,'idanioselect':int(soloAnio)}
    return render(render,'entidad_establecimiento.html',ctx,
    context_instance=RequestContext(request))

def numero_fallecidos(request):
    ctx = ""
    sumFallecidos = 0.0
    soloAnio = 0
    provincias = Provincia.objects.all()
    anios = Anios.objects.all()
    fallecidosPorProvincia = []
    fallecidosPorProvincia.append(['Provincia','Numero de fallecidos'])
    if request.method == 'POST':
        soloAnio = request.POST['selecccionarAnio']
        for cP in provincias:
            nEstablecimientos = Establecimiento.objects.filter(parroquia_idparroquia__canton_idcanton__provincia_idprovincia__idprovincia = cP.idprovincia,anios_idanios=soloAnio)
            for e in nEstablecimientos:
                sumFallecidos = sumFallecidos + e.numfallecidosmenor48horas
            fallecidosPorProvincia.append([smart_str(cP.nombreprovincia),sumFallecidos])
            sumFallecidos = 0
            print fallecidosPorProvincia
        print fallecidosPorProvincia
    ctx = {'provincias':provincias,'anios':anios,'fallecidosPorProvincia':fallecidosPorProvincia,'idanioselect':int(soloAnio)}
    return render(render,'numero_fallecidos.html',ctx,
    context_instance=RequestContext(request))
def numero_fallecidos_mayor(request):
    ctx = ""
    sumFallecidos = 0.0
    soloAnio = 0
    provincias = Provincia.objects.all()
    anios = Anios.objects.all()
    fallecidosPorProvincia = []
    fallecidosPorProvincia.append(['Provincia','Numero de fallecidos'])
    if request.method == 'POST':
        soloAnio = request.POST['selecccionarAnio']
        for cP in provincias:
            nEstablecimientos = Establecimiento.objects.filter(parroquia_idparroquia__canton_idcanton__provincia_idprovincia__idprovincia = cP.idprovincia,anios_idanios=soloAnio)
            for e in nEstablecimientos:
                sumFallecidos = sumFallecidos + e.numfallecidosmayor48horas
            fallecidosPorProvincia.append([smart_str(cP.nombreprovincia),sumFallecidos])
            sumFallecidos = 0
            print fallecidosPorProvincia
        print fallecidosPorProvincia
    ctx = {'provincias':provincias,'anios':anios,'fallecidosPorProvincia':fallecidosPorProvincia,'idanioselect':int(soloAnio)}
    return render(render,'numero_fallecidos_mayor.html',ctx,
    context_instance=RequestContext(request))
def comparacion_fallecidos(request):
    ctx = ""
    sumFallecidos = 0.0
    sumFallecidos1 =0.0
    soloAnio = 0

    provincias = Provincia.objects.all()
    anios = Anios.objects.all()
    fallecidosPorProvincia = []
    ctx = {'anios':anios}
    fallecidosPorProvincia.append(['Provincia','Numero de fallecidos menor a 48 horas','Numero de fallecidos mayor a 48 horas'])
    if request.method == 'POST':
        soloAnio = request.POST['selecccionarAnio']
        for cP in provincias:
            nEstablecimientos = Establecimiento.objects.filter(parroquia_idparroquia__canton_idcanton__provincia_idprovincia__idprovincia = cP.idprovincia,anios_idanios=soloAnio)
            for e in nEstablecimientos:
                sumFallecidos = sumFallecidos + e.numfallecidosmenor48horas
                sumFallecidos1 = sumFallecidos1 + e.numfallecidosmayor48horas
            fallecidosPorProvincia.append([smart_str(cP.nombreprovincia),sumFallecidos,sumFallecidos1])
            sumFallecidos = 0
            sumFallecidos1 = 0
    ctx = {'anios':anios, 'fallecidosPorProvincia':fallecidosPorProvincia,'idanioselect':int(soloAnio)}
    return render(render,'comparacion_fallecidos.html',ctx,
    context_instance=RequestContext(request))
def camas_provincia(request):
    ctx = ""
    soloAnio = 0
    lon = 0
    contEstablecimientos = 0
    listacamas = []
    tabla = []

    objAnios = Anios.objects.all()
    datos_enviados = []
    objProvincia = Provincia.objects.all()
    listacamas.append(['Clase de establecimientos','Numero de establecimientos'])
    numero_camas = 0
    contador = 1
    if request.method == 'POST':
        soloAnio = request.POST['selecccionarAnio']
        provincia = request.POST['provincia']
        datos_enviados.append({'provincia':provincia})
        print "Hola mundo "+str(soloAnio)
        numCamas = Camas.objects.all()
        especialidad = Servicioespecialidad.objects.all()
        prov = Provincia.objects.filter(idprovincia = provincia)

        for p in prov:
            nom_prov = p.nombreprovincia
        for a in especialidad:
            numcamas = Camas.objects.filter(servicioespecialidad_idservicioespecialidad = a.idservicioespecialidad, establecimiento_idestablecimiento__parroquia_idparroquia__canton_idcanton__provincia_idprovincia = provincia,establecimiento_idestablecimiento__anios_idanios = soloAnio)
            for b in numcamas:
                numero_camas += b.numcamasdisponibles

            listacamas.append([str(a.nombreservicioespecialidad), numero_camas])
            tabla.append([contador,nom_prov,smart_str(a.nombreservicioespecialidad), numero_camas])
            contador = contador + 1


    ctx = {'anios':objAnios,'establecimientoPorClase':listacamas,'datos':datos_enviados,'tabla':tabla,'idanioselect':int(soloAnio),'provincia':objProvincia }
    return render(render,'camas_provincia.html',ctx,context_instance=RequestContext(request))

def camas_dotacion(request):
    ctx = ""
    soloAnio = 0
    lon = 0
    contEstablecimientos = 0
    listacamas = []
    tabla = []

    objAnios = Anios.objects.all()
    datos_enviados = []

    listacamas.append(['Clase de establecimientos','Numero de establecimientos'])
    numero_camas = 0
    contador = 1
    if request.method == 'POST':
        soloAnio = request.POST['selecccionarAnio']
        parroquia = request.POST['parroquia']
        canton = request.POST['canton']
        provincia = request.POST['provincia']
        datos_enviados.append({'parroquia':parroquia, 'canton': canton, 'provincia':provincia})
        print "Hola mundo "+str(soloAnio)
        numCamas = Camas.objects.all()
        especialidad = Servicioespecialidad.objects.all()
        prov = Provincia.objects.filter(idprovincia = provincia)
        cant = Canton.objects.filter(idcanton = canton)
        parr = Parroquia.objects.filter(idparroquia = parroquia)
        for p in prov:
            nom_prov = p.nombreprovincia
        for c  in cant:
            nom_cant = c.nombrecanton
        for pa in parr:
            nom_par = pa.nombreparroquia
        for a in especialidad:
            numcamas = Camas.objects.filter(servicioespecialidad_idservicioespecialidad = a.idservicioespecialidad, establecimiento_idestablecimiento__parroquia_idparroquia__canton_idcanton__provincia_idprovincia = provincia,establecimiento_idestablecimiento__parroquia_idparroquia__canton_idcanton = canton,establecimiento_idestablecimiento__parroquia_idparroquia = parroquia,establecimiento_idestablecimiento__anios_idanios = soloAnio)
            for b in numcamas:
                numero_camas += b.numcamasdisponiblesdotacionnormal
            if numero_camas>0:

                listacamas.append([str(a.nombreservicioespecialidad), numero_camas])
                tabla.append([contador,nom_prov, nom_cant, nom_par,str(a.nombreservicioespecialidad), numero_camas])
            contador = contador + 1


    ctx = {'anios':objAnios,'establecimientoPorClase':listacamas,'datos':datos_enviados,'tabla':tabla,'idanioselect':int(soloAnio)}
    return render(render,'camas_dotacion.html',ctx,context_instance=RequestContext(request))

def json_anios(request):
    lista_anios = []
    anios = Anios.objects.all()
    for c in anios:
        lista_anios.append({'id_anio':c.idanios,'anio':c.anio})
    return HttpResponse(json.dumps(lista_anios), content_type='json')

def json_provincias(request):
    lista_provincias = []
    provincias = Provincia.objects.all()
    for c in provincias:
        lista_provincias.append({'id_provincia':c.idprovincia,'provincia':c.nombreprovincia})
    return HttpResponse(json.dumps(lista_provincias), content_type='json')

def json_cantones(request,valorunic):
    lista_canton = []
    cantones = Canton.objects.filter(provincia_idprovincia = valorunic)
    for c in cantones:
        lista_canton.append({'id_canton':c.idcanton,'canton':c.nombrecanton})
    return HttpResponse(json.dumps(lista_canton), content_type='json')

def json_parroquias(request, provincia, canton):
    lista_parroquia = []
    parroquias = Parroquia.objects.filter(canton_idcanton = canton, canton_idcanton__provincia_idprovincia = provincia)
    for c in parroquias:
        lista_parroquia.append({'id_parroquia':c.idparroquia,'parroquia':c.nombreparroquia})
    return HttpResponse(json.dumps(lista_parroquia), content_type='json')
