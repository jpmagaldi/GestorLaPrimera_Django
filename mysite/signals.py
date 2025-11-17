from django.db.models.signals import post_migrate
from django.dispatch import receiver
from mysite.models import *
from django.utils import timezone
from django.contrib.auth import get_user_model



@receiver(post_migrate)
def crear_registros_iniciales(sender, **kwargs):
    if sender.name == 'mysite':
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
            ahora = timezone.now()
            Productos.objects.create(nombre='PAN DE PANCHO X6', lista=lista_obj, precio=1200.00, fecha=ahora, iva='21.0')
            Productos.objects.create(nombre='PAN DE MIGA 1X10', lista=lista_obj1, precio=1500.00, fecha=ahora, iva='21.0')
        if not Clientes.objects.exists():
            Clientes.objects.create(cuit='30716920093', razons= 'ASD SISTEMAS MEDICOS',
                direccion='UGARTE MANUEL 3867 Piso:3 Dpto:H', provincia=Zonas.objects.get(id=0),
                lista=lista_obj, responsabilidad=respiva_obj, descuento=0, recargo=0)
        if not Comprobantes.objects.exists():
            Comprobantes.objects.create(descripcion='FACTURA A', codigo='001')
            Comprobantes.objects.create(descripcion='FACTURA B', codigo='006')
            Comprobantes.objects.create(descripcion='FACTURA C', codigo='011')
            Comprobantes.objects.create(descripcion='NOTA DE CREDITO A', codigo='003')
            Comprobantes.objects.create(descripcion='NOTA DE CREDITO B', codigo='008')
            Comprobantes.objects.create(descripcion='NOTA DE CREDITO C', codigo='013')
            Comprobantes.objects.create(descripcion='TIQUE', codigo='083')
        if not Configuracion.objects.exists():
            Configuracion.objects.create(punto_venta='00040')


    User = get_user_model()
    username = 'admin'
    email = 'admin@example.com'
    password = '1234'

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
