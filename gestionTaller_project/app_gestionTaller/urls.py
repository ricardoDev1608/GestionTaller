from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("clientes/", views.lista_clientes_web, name="lista_clientes"),
    path("clientes/<int:cliente_id>/", views.detalle_cliente_web, name="detalle_cliente_web"),
    path("clientes/nuevo/", views.nuevo_cliente, name="nuevo_cliente"),
    path("coches/", views.lista_coches_web, name="lista_coches"),
    path("coches/nuevo/", views.nuevo_coche, name="nuevo_coche"),
    path("coches/<int:coche_id>/servicios/", views.servicios_coche_web, name="servicios_coche_web"),
    path("servicios/", views.lista_servicios_web, name="lista_servicios"),
    path("servicios/nuevo/", views.nuevo_servicio, name="nuevo_servicio"),
    path("coches-servicios/nuevo/", views.nuevo_coche_servicio, name="nuevo_coche_servicio"),
    path("api/clientes/", views.lista_clientes, name="api_lista_clientes"),
    path("api/clientes/<int:cliente_id>/", views.detalle_cliente, name="api_detalle_cliente"),
    path("api/registrar-cliente/", views.registrar_cliente, name="api_registrar_cliente"),
    path("api/registrar-coche/", views.registrar_coche, name="api_registrar_coche"),
    path("api/registrar-servicio/", views.registrar_servicio, name="api_registrar_servicio"),
    path("api/buscar-cliente/<int:cliente_id>/", views.buscar_cliente, name="api_buscar_cliente"),
    path(
        "api/buscar-coche-por-matricula/<str:matricula>/",
        views.buscar_coche_por_matricula,
        name="api_buscar_coche_por_matricula",
    ),
    path(
        "api/buscar-coches-de-cliente/<int:cliente_id>/",
        views.buscar_coches_de_cliente,
        name="api_buscar_coches_de_cliente",
    ),
    path(
        "api/buscar-servicios-de-coche/<int:coche_id>/",
        views.buscar_servicios_de_coche,
        name="api_buscar_servicios_de_coche",
    ),
]
