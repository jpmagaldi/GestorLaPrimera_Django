# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal



class Clientes(models.Model):
    cuit = models.CharField(max_length=13, unique=True)
    razons = models.CharField(max_length=60)  
    direccion = models.CharField(max_length=45)  
    provincia = models.ForeignKey('Zonas', on_delete=models.PROTECT, blank=True, null=True)
    alias = models.CharField(max_length=45, blank=True)
    lista = models.ForeignKey('Listas', on_delete=models.PROTECT)
    responsabilidad = models.ForeignKey('RespIva', on_delete=models.PROTECT)  
    descuento = models.DecimalField(max_digits=2, decimal_places=2, default=0.00, validators=[MinValueValidator(Decimal('0'))])
    recargo = models.DecimalField(max_digits=2, decimal_places=2, default=0.00, validators=[MinValueValidator(Decimal('0'))])

    def __str__(self):
        return self.razons
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class RespIva(models.Model):
    descripcion = models.CharField(unique=True, max_length=45)  

    def __str__(self):
        return self.descripcion
    
    class Meta:
        verbose_name = "RespIva"
        verbose_name_plural = "RespIva"

class Zonas(models.Model):
    nombre = models.CharField(max_length=45, unique=True)
    dgr = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Zona"
        verbose_name_plural = "Zonas"

class Listas(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Lista"
        verbose_name_plural = "Listas"

class Productos(models.Model):
    IVA_CHOICES = {
    "10.5": "10.5%",
    "21.0": "21%",
    }
    
    lista = models.ForeignKey(Listas, models.CASCADE)  
    nombre = models.CharField(max_length=70)
    precio = models.CharField(max_length=13) #DECIMAL TIENE QUE SER
    fecha = models.DateField()
    iva = models.CharField(max_length=4, choices=IVA_CHOICES, default='21.0')

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        unique_together = (('lista', 'nombre'),)

    def __str__(self):
        return (self.nombre)

class Comprobantes(models.Model):
    descripcion = models.CharField(unique=True, max_length=45)
    codigo = models.CharField(max_length=3)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name = "Comprobante"
        verbose_name_plural = "Comprobantes"

class Ventas(models.Model):
    fecha = models.DateField()
    comprobante = models.ForeignKey(Comprobantes, on_delete=models.PROTECT)
    n_fact = models.CharField(max_length=14)
    cliente = models.ForeignKey(Clientes, on_delete=models.PROTECT)
    pan105 = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    pan21 = models.DecimalField(max_digits=9, decimal_places=2, default=0.00) 
    exento = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    iva105 = models.DecimalField(max_digits=9, decimal_places=2, default=0.00) 
    iva21 = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    otros = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    class Meta:
        unique_together = (('cliente', 'comprobante', 'n_fact'),)
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def __str__(self):
       return self.n_fact

class VentaProductos(models.Model):
    comprobante = models.ForeignKey(Comprobantes, models.PROTECT) 
    n_fact = models.ForeignKey(Ventas, models.CASCADE)
    producto = models.CharField(max_length=45)
    cantidad = models.CharField(max_length=10)
    precio_u = models.DecimalField(max_digits=9, decimal_places=4)
    total = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.n_fact.n_fact
    
    class Meta:
        verbose_name = "VentaProductos"
        verbose_name_plural = "VentaProductos"


class Configuracion(models.Model):
    punto_venta = models.CharField(max_length=5)

    def __str__(self):
        return self.punto_venta
    
    class Meta:
        verbose_name = "Configuracion"
        verbose_name_plural = "Configuracion"