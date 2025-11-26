"""
URL configuration for Gestor_LaPrimeraDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mysite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    
    path('abmclientes/', views.abmClientes, name='abmClientes'),
    path('api/internal/abmclientes/guadar_cliente/', views.guardarCliente, name='guardarCliente'),
    path('api/internal/abmclientes/editar_clientes/', views.editarCliente, name='editarCliente'),
    path('api/internal/abmclientes/borrar_clientes/', views.borrarCliente, name='borrarCliente'),
    path('api/internal/abmclientes/buscar_clientes/', views.buscarCliente, name='buscarCliente'),
    path('api/internal/abmclientes/error_arca/', views.errorArca, name='errorArca'),

    path('facturador/', views.facturador, name='facturador'),
    path('api/internal/facturador/buscar_clientes/<str:Cliente>', views.buscar_clientes, name='buscar_clientes'),
    path('api/internal/facturador/seleccionar_cliente/<str:Cliente>', views.select_cliente, name='select_clientes'),
    path('api/internal/facturador/buscar_productos/<str:Nombre>/<str:Lista>', views.buscar_productos, name='buscar_productos'),
    path('api/internal/facturador/obt-nrofact/', views.obtener_nrofact, name='obtener_nrofact'),
    path('api/internal/facturador/generarFactura/', views.generarFactura, name='generarFactura'),
    
    path('reportes/ventas', views.reportesVentas, name='reportesVentas'),
    path('reportes/ventas/ver-factura/<str:Comprobante>/<str:Nro>/', views.verFactura, name='verFactura'),
    path('api/internal/reportes/ventas/reporte-por-fecha/<str:fechaIni>/<str:fechaFin>/', views.busquedaVentas, name='busquedaVentas'),
    path('api/internal/conectar-wsaa/', views.conectar_wsaa, name='conectar_wsaa'),

]
