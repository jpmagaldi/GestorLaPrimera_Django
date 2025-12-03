from django.shortcuts import render
from .models import *
from datetime import datetime
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.template.loader import render_to_string
from django.db.models import ProtectedError
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.urls import reverse
from .Afip.wsaa import WSAA
from .Afip.wsfev1 import WSFEv1
from .Afip.ws_sr_padron import WSSrPadronA5
import os
from asgiref.sync import sync_to_async

from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

import json
from base64 import b64encode
import qrcode
from io import BytesIO
import base64

def home(request):
	return render(request, 'home.html')

@never_cache
def abmClientes(request):
	zonas = Zonas.objects.all().order_by('nombre')
	listas = Listas.objects.all().order_by('nombre')
	resp = RespIva.objects.all().order_by('descripcion')
	clientes = Clientes.objects.all().order_by('razons')
	url_base = reverse('abmClientes')
	
	context = {
		'prov' : zonas,
		'listas' : listas,
		'resp' : resp,
		'clientes': clientes,
		'url_base': url_base
	}

	return render(request, 'clientes.html', {'context': context})

@require_POST
def guardarCliente(request):
	newcuit = request.POST.get('cuit')
	oldcuit = request.POST.get('oldCuit')
	errInput = request.POST.get('errorInput')
	if errInput:
		messages.error(request, "ARCA devolvió un error al ingresar ese CUIT")
		return redirect(request.META.get('HTTP_REFERER', '/'))
	
	if len(newcuit) != 11:
		messages.error(request, "El CUIT debe tener 11 valores numericos.")
		return redirect(request.META.get('HTTP_REFERER', '/'))
   
	accionInput = request.POST.get('accionInput')
	if Clientes.objects.filter(cuit=newcuit).exists() and accionInput == 'guardar':
		messages.error(request, "El cliente con ese CUIT ya existe.")
		return redirect(request.META.get('HTTP_REFERER', '/'))
	provincia = request.POST.get('prov')
	lista = request.POST.get('lista')
	resp = request.POST.get('resp')
	provincia = Zonas.objects.get(nombre=request.POST.get('prov'))
	lista = Listas.objects.get(nombre=request.POST.get('lista'))
	resp = RespIva.objects.get(descripcion=request.POST.get('resp'))
	
	Clientes.objects.update_or_create(cuit=oldcuit, defaults={
		'cuit':newcuit,
		'razons':request.POST.get('razons'),
		'direccion':request.POST.get('dir'),
		'provincia':provincia,
		'alias':request.POST.get('alias'),
		'lista':lista,
		'responsabilidad':resp,
		'descuento':request.POST.get('desc'),
		'recargo':request.POST.get('rec')
	})
	messages.success(request, "Cliente creado correctamente.")
	return redirect(request.META.get('HTTP_REFERER', '/'))

def editarCliente(request):
	query = request.GET.get('q', '')
	cliente = Clientes.objects.get(cuit=query)
	return JsonResponse({
		'razons': cliente.razons,
		'dir': cliente.direccion,
		'prov': cliente.provincia.nombre,
		'alias': cliente.alias,
		'lista': cliente.lista.nombre,
		'resp': cliente.responsabilidad.descripcion,
		'desc': cliente.descuento,
		'rec': cliente.recargo,
	})

@require_POST
def borrarCliente(request):
	query = request.POST.get('bCuit')
	try:
		Clientes.objects.get(cuit=query).delete()
		messages.success(request, "Cliente eliminado correctamente.")
	except ProtectedError:
		messages.error(request, "Accion denegada. El cliente tiene facturas relacionadas.")
	except PermissionDenied:
		messages.error(request, "No tenés permiso para eliminar este cliente.")
	except Exception as e:
		messages.error(request, f"Ocurrió un error inesperado: {str(e)}")
	
	return redirect(request.META.get('HTTP_REFERER', '/'))

def buscarCliente(request):
	global Padron
	query = request.GET.get('q', '')
	try:
		Padron.Consultar(query)
		err2 = False
		if Padron.imp_iva in ['N', 'NI']:
			err = True
			codigo = '1010'
		else:
			err = False
		if Padron.imp_iva in ['AC', 'S']:
			resp = 'RESPONSABLE INSCRIPTO'
		elif Padron.imp_iva == 'EX':
			resp = 'EXENTO'
		else:
			resp = ''
	except:
		err2 = True
		codigo = '1011'
		resp = ''
		err = False

	return JsonResponse({
		'razons': Padron.denominacion,
		'dir': Padron.direccion,
		'resp': resp,
		'err': err,
		'prov': Padron.provincia,
		'codigo': codigo,
		'err2': err2
	})

@never_cache
def errorArca(request):
	if request.GET.get('codigo') not in ['1010','1011']:
		return HttpResponseForbidden("Acceso denegado")
	if request.GET.get('codigo') == '1010':
		messages.error(request, "Error en ARCA. CUIT dudoso")
	else:
		messages.error(request, "Error en ARCA. CUIT Inválido")
	return redirect(request.META.get('HTTP_REFERER', '/'))


def reportesVentas(request):
	url_verFactura = reverse('verFactura', args=['Comprobante', 'Nro'])
	url_reportFechaFSR = reverse('busquedaVentasFSR', args=['fechaIni', 'fechaFin'])
	url_reportFechaFCR = reverse('busquedaVentasFCR', args=['fechaIni', 'fechaFin', 'razonS'])
	url_reportFechaRSF = reverse('busquedaVentasRSF', args=['razonS'])
	
	context = {
		'url_template': {
			'url_verFactura': url_verFactura,
			'url_reportFechaFSR': url_reportFechaFSR,
			'url_reportFechaFCR': url_reportFechaFCR,
			'url_reportFechaRSF': url_reportFechaRSF
		},	
	}
	return render(request, 'reportesVentas.html', context)

def busquedaVentas(request, fechaIni=None, fechaFin=None, razonS=None):
	if ViewToken(request.META.get("HTTP_X_INTERNAL_TOKEN")):
		return HttpResponseForbidden("Acceso denegado")
	if fechaIni:
		FechaInicio = datetime.strptime(fechaIni, '%d-%m-%Y').date()
		FechaFin = datetime.strptime(fechaFin, '%d-%m-%Y').date()
		if razonS:
			Report = Ventas.objects.filter(fecha__range=(FechaInicio, FechaFin), cliente__razons__contains=razonS).values(
			'fecha',
			'comprobante__descripcion',
			'n_fact',
			'cliente__razons',
			'total',
			)
		else:
			Report = Ventas.objects.filter(fecha__range=(FechaInicio, FechaFin)).values(
			'fecha',
			'comprobante__descripcion',
			'n_fact',
			'cliente__razons',
			'total',
			)
	else: 
		if razonS:
			Report = Ventas.objects.filter(cliente__razons__contains=razonS).values(
			'fecha',
			'comprobante__descripcion',
			'n_fact',
			'cliente__razons',
			'total',
			)

	if Report.exists():
		return JsonResponse({
			'facturas': list(Report),
		})
	else:
		return JsonResponse({
			'facturas': [],
		})

def verFactura(request, Comprobante, Nro):
	factura = Ventas.objects.get(comprobante__descripcion=Comprobante, n_fact=Nro)
	itemFactura = VentaProductos.objects.filter(n_fact=factura)
	subtotal = float(factura.pan21) + float(factura.pan105)

	context = {
		'factura': factura,
		'itemFactura': itemFactura,
		'subtotal' : subtotal
	}

	return render(request, 'detalleFactura.html', context)


@never_cache
def facturador(request):
	fecha = datetime.today().strftime('%d/%m/%Y')
	clientes = Clientes.objects.all()

	contexto = {
		'url_template': {
			'url_bClientes': reverse('buscar_clientes', args=['Cliente']),
			'url_sCliente': reverse('select_clientes', args=['Cliente']),
			'url_bProductos': reverse('buscar_productos', args=['Nombre', 'Lista']),
			'url_wsaa': reverse('conectar_wsaa')
		},
		'fecha':fecha,
		'clientes':clientes}
	
	return render(request, 'facturador.html', contexto)

def buscar_clientes(request, Cliente):
	if ViewToken(request.META.get("HTTP_X_INTERNAL_TOKEN")):
		if Cliente:
			clientes = Clientes.objects.filter(razons__icontains=Cliente)[:10]
		else:
			clientes = Clientes.objects.all()
		resultados = list(clientes.values('cuit', 'razons')) 
		return JsonResponse({'clientes': resultados})

def select_cliente(request, Cliente):
	if ViewToken(request.META.get("HTTP_X_INTERNAL_TOKEN")):
		return HttpResponseForbidden("Acceso denegado")
	if Cliente:
		clientes = Clientes.objects.filter(cuit__exact=Cliente)
	resultados = list(clientes.values('razons', 'cuit', 'direccion', 'responsabilidad__descripcion', 'lista__nombre'))
	return JsonResponse({'dato_cli': resultados})

def buscar_productos(request, Nombre, Lista):
	if ViewToken(request.META.get("HTTP_X_INTERNAL_TOKEN")):
		return HttpResponseForbidden("Acceso denegado")

	if Nombre and Lista:
		productos = Productos.objects.filter(lista__nombre=Lista).filter(nombre__icontains=Nombre)
	else:
		productos = Productos.objects.filter(lista=Lista)
	resultados = list(productos.values())
	return JsonResponse({'productos': resultados})

@require_POST
def generarFactura(request):  
	try:
		global letra
		match letra:
			case 1:
				Comp = 'A'
				comp = 'FACTURA A'
				Cod = '001'
			case 6:
				Comp = 'B'
				comp = 'FACTURA B'
				Cod = '006'
			case 3:
				Comp = 'A'
				comp = 'NOTA DE CREDITO A'
				Cod = '003'
			case 8:
				Comp = 'B'
				comp = 'NOTA DE CREDITO B'
				Cod = '008'
		
		Fecha=request.POST.get('date')
		N_fact=request.POST.get('Nrofact')
		Razons=request.POST.get('razons')
		Dir=request.POST.get('dir')
		Cuit=request.POST.get('cuit')
		Resp=request.POST.get('resp')
		Pan105=request.POST.get('neto105')
		Pan21=request.POST.get('neto21')
		Iva105=request.POST.get('iva105')
		Iva21=request.POST.get('iva21')
		Total=request.POST.get('total')
		Prod = json.loads(request.POST.get('inputJson'))
		radio=request.POST.get('toggle')
		
		global Wsfe

		punto_vta = int(N_fact.split('-')[0])
		cbte_nro = int(N_fact.split('-')[1])
		nro_doc = Cuit.replace('-','')
		imp_total = Total.split(' ')[1]
		imp_neto = str(round((float(Pan105.split(' ')[1]) + float(Pan21.split(' ')[1])),2))
		imp_iva = str(round((float(Iva105.split(' ')[1]) + float(Iva21.split(' ')[1])),2))
		fecha_cbte = datetime.now().strftime("%Y%m%d")
		

		Wsfe.CrearFactura(
			concepto=1, nro_doc=nro_doc, tipo_cbte=letra,
			cbt_desde=cbte_nro , cbt_hasta=cbte_nro, fecha_cbte=fecha_cbte,
			punto_vta=punto_vta, imp_total=imp_total,
			imp_neto=imp_neto, imp_iva=imp_iva,
			condicion_iva_receptor_id=1
		)

		if Pan21.split(' ')[1] != '0.00':
			Wsfe.AgregarIva(5, round(float(Pan21.split(' ')[1]),2), round(float(Iva21.split(' ')[1]),2))

		if Pan105.split(' ')[1] != '0.00':
			Wsfe.AgregarIva(4, round(float(Pan105.split(' ')[1]),2), round(float(Iva105.split(' ')[1]),2))
		
		
		if radio == 'credito':
			Wsfe.AgregarPeriodoComprobantesAsociados(fecha_cbte, fecha_cbte)

		
		Wsfe.CAESolicitar()

		#print(Wsfe.ErrMsg)
		#print(Wsfe.Obs)
		#print(Wsfe.CAE)

		if Wsfe.CAE == '':
			messages.error(request, "Problemas al generar la factura: %s  |  %s" % (Wsfe.Obs, Wsfe.ErrMsg))
			return redirect(request.META.get('HTTP_REFERER', '/'))

		vto = Wsfe.Vencimiento[-2:] + '/' \
			+ Wsfe.Vencimiento[-4:-2] + '/' \
			+ Wsfe.Vencimiento[:4]

		afip = 'https://www.arca.gob.ar/fe/qr/?p='
		
		aux = { "ver":1,"fecha":datetime.now().strftime("%Y-%m-%d"),
			"cuit":Wsfe.Cuit,"ptoVta":punto_vta,"tipoCmp":letra,
			"nroCmp":cbte_nro,"importe":float(imp_total),"moneda":"PES",
			"ctz":"1.000","tipoDocRec":80,"nroDocRec":int(nro_doc),
			"tipoCodAut":"E","codAut":int(Wsfe.CAE) }
			
		code = b64encode(json.dumps(aux).encode('utf-8'))
		code = code.decode('utf-8')
		qr = afip + code
		
		datos_factura = {
			'Fecha': Fecha,
			'Comp': Comp,
			'Cod' : Cod,
			'N_fact': N_fact,
			'Razons': Razons,
			'Cuit': Cuit,
			'Dir': Dir,
			'Resp': Resp,
			'productos': Prod,
			'subtotal': imp_neto,
			'iva105': Iva105.split(' ')[1],
			'iva21': Iva21.split(' ')[1],
			'total': imp_total,
			'cae': Wsfe.CAE,
			'vto': vto,
			'qr': qr,
		}
		
		factObj = Ventas.objects.create(
			fecha= datetime.strptime(Fecha, "%d/%m/%Y").strftime("%Y-%m-%d"),
			comprobante= Comprobantes.objects.get(descripcion=comp),
			n_fact=N_fact,
			cliente= Clientes.objects.get(cuit=Cuit),
			pan105=Pan105.split(' ')[1],
			pan21=Pan21.split(' ')[1],
			exento= '0.00',
			iva105=Iva105.split(' ')[1],
			iva21=Iva21.split(' ')[1],
			otros= '0.00',
			total=Total.split(' ')[1]
		)

		for producto in Prod:
			VentaProductos.objects.create(
				comprobante = factObj.comprobante,
				n_fact = factObj,
				producto = producto['descripcion'],
				cantidad = producto['cantidad'],
				precio_u = producto['precio'],
				total = producto['subtotal']
			)
	
		html = render_to_string('factura.html', {'datos': datos_factura})
		return HttpResponse(html)
	except Exception as e:   
		messages.error(request, "Problemas internos: %s" % e)
		return redirect(request.META.get('HTTP_REFERER', '/'))


@sync_to_async
def obtener_Config():
	return Configuracion.objects.first()

async def conectar_wsaa(request):
	ViewToken(request)

	ruta_base = os.path.dirname(__file__)  # Carpeta donde está views.py
	CrtProd = os.path.join(ruta_base, 'static\cert\\productioncrt.crt')
	KeyProd = os.path.join(ruta_base, 'static\cert\\productionKEY.key')
	Crt = os.path.join(ruta_base, 'static\cert\\testingCRT.crt')
	Key = os.path.join(ruta_base, 'static\cert\\testingKey.key')
	msg = ''
	err = 0
	try:
		query = request.GET.get('q', '')
		if query == 'wsfe':
			global Wsfe
			Wsfe = WSFEv1()
			Wsfe.SetTicketAcceso(
				WSAA().Autenticar(query, Crt, Key))
			Wsfe.Cuit = 20218452788
			await obtener_Config()
			Wsfe.Conectar()
		elif query == 'ws_sr_constancia_inscripcion':
			global Padron
			Padron = WSSrPadronA5()
			Padron.SetTicketAcceso(
				WSAA().Autenticar("ws_sr_constancia_inscripcion", CrtProd, KeyProd))
			Padron.Cuit = 30670206528
			Padron.Conectar()
	except Exception as e:
		print(str(e))
		if str(e) == 'key values mismatch':
			err = 1
			msg = 'Error: La clave privada no coincide con el certificado'
		elif str(e).startswith('Unable to find the server'):
			err = 2
			msg = 'El servidor de ARCA no está disponible, revise que tenga internet tambien.'
		elif str(e).startswith('ns1:cms.cert.untrusted: Certificado'):
			err = 2
			msg = 'Certificado no emitido por AC de confianza.'
	return JsonResponse({'mensaje': msg, 'err': err})

async def obtener_nrofact(request):
	try:
		ViewToken(request)
		global Wsfe, letra
		query = request.GET.get('q', '')
		letra = int(query)
		config = await obtener_Config() 
		comprobante = Wsfe.CompUltimoAutorizado(int(query), int(config.punto_venta))
		return JsonResponse(
			{'Nrofact': config.punto_venta.zfill(5) + '-' + str(int(comprobante) + 1).zfill(8)})
	except:
		return redirect('facturador.html')

def ViewToken(token):
	if token is None or token != 'token-seguro-123':
		return True
	else: 
		return False