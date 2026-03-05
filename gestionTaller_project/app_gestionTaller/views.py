from django.http import JsonResponse
from .models import Cliente
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Cliente, Coche, Servicio, CocheServicio


def lista_clientes(request):
    clientes = list(Cliente.objects.values("id", "nombre", "telefono", "email"))
    return JsonResponse(clientes, safe=False)

def detalle_cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.values("id", "nombre", "telefono", "email").get(id=cliente_id)
        return JsonResponse(cliente)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)