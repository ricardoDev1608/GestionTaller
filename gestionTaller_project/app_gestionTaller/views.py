from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import json
from .models import Cliente, Coche, Servicio, CocheServicio
from .forms import ClienteForm, CocheForm, ServicioForm, CocheServicioForm


def lista_clientes(request):
    clientes = list(Cliente.objects.values("id", "nombre", "telefono", "email"))
    return JsonResponse(clientes, safe=False)

def detalle_cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.values("id", "nombre", "telefono", "email").get(id=cliente_id)
        return JsonResponse(cliente)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)


@csrf_exempt
def registrar_cliente(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.create(
                nombre=data["nombre"],
                telefono=data["telefono"],
                email=data["email"]
            )
            return JsonResponse({"mensaje": "Cliente registrado con éxito", "cliente_id": cliente.id})
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def registrar_coche(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.get(id=data["cliente_id"])
            coche = Coche.objects.create(
                cliente=cliente,
                marca=data["marca"],
                modelo=data["modelo"],
                matricula=data["matricula"]
            )
            return JsonResponse({"mensaje": "Coche registrado con éxito", "coche_id": coche.id})
        except Cliente.DoesNotExist:
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def registrar_servicio(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            coche = Coche.objects.get(id=data["coche_id"])
            servicio = Servicio.objects.create(
                nombre=data["nombre"],
                descripcion=data["descripcion"]
            )
            CocheServicio.objects.create(coche=coche, servicio=servicio)
            return JsonResponse({"mensaje": "Servicio registrado con éxito", "servicio_id": servicio.id})
        except Coche.DoesNotExist:
            return JsonResponse({"error": "Coche no encontrado"}, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def buscar_cliente(request, cliente_id):
    if request.method == "GET":
        try:
            cliente = Cliente.objects.values("id", "nombre", "telefono", "email").get(id=cliente_id)
            return JsonResponse(cliente)
        except Cliente.DoesNotExist:
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def buscar_coche_por_matricula(request, matricula):
    if request.method == "GET":
        try:
            coche = Coche.objects.select_related("cliente").get(matricula=matricula)
            return JsonResponse({
                "coche": {
                    "id": coche.id,
                    "marca": coche.marca,
                    "modelo": coche.modelo,
                    "matricula": coche.matricula
                },
                "cliente": {
                    "id": coche.cliente.id,
                    "nombre": coche.cliente.nombre,
                    "telefono": coche.cliente.telefono,
                    "email": coche.cliente.email
                }
            })
        except Coche.DoesNotExist:
            return JsonResponse({"error": "Coche no encontrado"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def buscar_coches_de_cliente(request, cliente_id):
    if request.method == "GET":
        if not Cliente.objects.filter(id=cliente_id).exists():
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)
        coches = list(
            Coche.objects.filter(cliente_id=cliente_id).values("id", "marca", "modelo", "matricula")
        )
        return JsonResponse(coches, safe=False)
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def buscar_servicios_de_coche(request, coche_id):
    if request.method == "GET":
        try:
            coche = Coche.objects.get(id=coche_id)
            servicios = list(
                CocheServicio.objects.filter(coche=coche)
                .select_related("servicio")
                .values("servicio__id", "servicio__nombre", "servicio__descripcion")
            )
            return JsonResponse({
                "coche": {
                    "id": coche.id,
                    "marca": coche.marca,
                    "modelo": coche.modelo,
                    "matricula": coche.matricula
                },
                "servicios": servicios
            })
        except Coche.DoesNotExist:
            return JsonResponse({"error": "Coche no encontrado"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)


def inicio(request):
    return render(request, "inicio.html")


def lista_clientes_web(request):
    clientes = Cliente.objects.all()
    return render(request, "clientes.html", {"clientes": clientes})


def detalle_cliente_web(request, cliente_id):
    try:
        cliente = Cliente.objects.get(id=cliente_id)
        coches = Coche.objects.filter(cliente=cliente)

        contexto = {
            "cliente": cliente,
            "coches": coches,
        }

        return render(request, "detalle_cliente.html", contexto)

    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)


def lista_coches_web(request):
    coches = Coche.objects.select_related("cliente").all()
    return render(request, "coches.html", {"coches": coches})


def lista_servicios_web(request):
    servicios = Servicio.objects.all()
    return render(request, "servicios.html", {"servicios": servicios})


def nuevo_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_clientes")
    else:
        form = ClienteForm()
    return render(request, "formulario.html", {"form": form, "titulo": "Nuevo Cliente"})


def nuevo_coche(request):
    if request.method == "POST":
        form = CocheForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_coches")
    else:
        form = CocheForm()
    return render(request, "formulario.html", {"form": form, "titulo": "Nuevo Coche"})


def nuevo_servicio(request):
    if request.method == "POST":
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_servicios")
    else:
        form = ServicioForm()
    return render(request, "formulario.html", {"form": form, "titulo": "Nuevo Servicio"})


def nuevo_coche_servicio(request):
    if request.method == "POST":
        form = CocheServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_servicios")
    else:
        form = CocheServicioForm()
    return render(request, "formulario.html", {"form": form, "titulo": "Nueva Relación Coche-Servicio"})
