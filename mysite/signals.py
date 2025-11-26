from django.db.models.signals import post_migrate
from django.dispatch import receiver
from mysite.models import *
from django.utils import timezone
from django.contrib.auth import get_user_model



@receiver(post_migrate)
def crear_registros_iniciales(sender, **kwargs):
    if sender.name == 'mysite':
        ahora = timezone.now()
        if not RespIva.objects.exists():
            respiva_obj = RespIva.objects.create(descripcion='RESPONSABLE INSCRIPTO')
            RespIva.objects.create(descripcion='EXENTO')
            RespIva.objects.create(descripcion='MONOTRIBUTO')
        if not Zonas.objects.exists():
            zonas = ['CIUDAD AUTONOMA BUENOS AIRES','BUENOS AIRES','CATAMARCA','CORDOBA','CORRIENTES','ENTRE RIOS',
                'JUJUY','MENDONZA','LA RIOJA','SALTA','SAN JUAN','SAN LUIS','SANTA FE', 'SANTIAGO DEL ESTERO', 'TUCUMAN', 'CHACO',
                'CHUBUT','FORMOSA','MISIONES','NEUQUEN','LA PAMPA','RIO NEGRO','SANTA CRUZ','TIERRA DEL FUEGO']
            i = 0
            for zona in zonas:
                Zonas.objects.create(id=i, nombre=zona, dgr=0)
                i += 1
        if not Listas.objects.exists():
            lista_obj = Listas.objects.create(nombre='SUPERMERCADOS')
            lista_obj1 = Listas.objects.create(nombre='MINORISTAS')
        if not Productos.objects.exists():
            Productos.objects.create(nombre='PAN DE PANCHO X6', lista=lista_obj, precio=1200.00, fecha=ahora, iva='21.0')
            Productos.objects.create(nombre='PAN DE MIGA 1X10', lista=lista_obj1, precio=1500.00, fecha=ahora, iva='21.0')
        if not Clientes.objects.exists():
            Clien_obj = Clientes.objects.create(cuit='30202020204', razons= 'CLIENTE FALSO',
                direccion='CALLE FALSA 123', provincia=Zonas.objects.get(id=0),
                lista=lista_obj, responsabilidad=respiva_obj, descuento=0, recargo=0)
        if not Comprobantes.objects.exists():
            Comp_obj = Comprobantes.objects.create(descripcion='FACTURA A', codigo='001')
            Comprobantes.objects.create(descripcion='FACTURA B', codigo='006')
            Comprobantes.objects.create(descripcion='FACTURA C', codigo='011')
            Comprobantes.objects.create(descripcion='NOTA DE CREDITO A', codigo='003')
            Comprobantes.objects.create(descripcion='NOTA DE CREDITO B', codigo='008')
            Comprobantes.objects.create(descripcion='NOTA DE CREDITO C', codigo='013')
            Comprobantes.objects.create(descripcion='TIQUE', codigo='083')
        if not Configuracion.objects.exists():
            Configuracion.objects.create(punto_venta='00040')
        if not Ventas.objects.exists():
            Venta_obj = Ventas.objects.create(
                fecha= ahora,
                comprobante= Comp_obj, n_fact= '00041-00000040',
                cliente= Clien_obj,
                pan105= 0.00, pan21=991.7355, exento=0.00,
                iva21=208.2644, iva105=0.00,
                otros=0.00, total=1200.00)
        if not VentaProductos.objects.exists():
            VentaProductos.objects.create(
                comprobante=Comp_obj,
                n_fact=Venta_obj,
                producto='PAN DE PANCHO X6',
                cantidad= 1,
                precio_u= 991.7355,
                total= 991.73
            )



    User = get_user_model()
    username = 'admin'
    email = 'admin@example.com'
    password = '1234'

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
