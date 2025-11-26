from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Comprobantes)
admin.site.register(RespIva)
admin.site.register(Zonas)
admin.site.register(Listas)



@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ["razons", "cuit", 'responsabilidad', 'lista', 'alias']
    search_fields = ('razons', 'cuit')
    
@admin.register(Ventas)
class VentasAdmin(admin.ModelAdmin):
    def cliente_name(self, obj):
        return obj.cliente.nombre    
    
    list_display = ["fecha", "comprobante", 'n_fact', 'cliente', 'total']
    search_fields = ('fecha', 'comprobante__descripcion', 'cliente__razons')
    list_filter = ('fecha','comprobante')

@admin.register(Configuracion)
class ConfiguracionAdmin(admin.ModelAdmin):
    list_display = ['punto_venta']

@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ["nombre", "lista", 'precio', 'fecha']
    search_fields = ('nombre', "lista")
    list_filter = ('lista',)

@admin.register(VentaProductos)
class VentaProductosAdmin(admin.ModelAdmin):    
    list_display = ["n_fact", "comprobante", 'producto', 'cantidad', 'total']
    search_fields = ('n_fact', 'comprobante__descripcion')