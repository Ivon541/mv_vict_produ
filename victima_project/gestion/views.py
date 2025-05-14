
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Turno, HistorialAccion
from collections import deque

# Estructuras en memoria (podrías hacerlas persistentes si deseas)
cola_turnos = deque()
pila_historial = []

@login_required
def agregar_turno(request):
    turno = Turno.objects.create(usuario=request.user)
    cola_turnos.append(turno.id)
    registrar_accion(request.user, "Solicitó un turno")
    return redirect('ver_turnos')

@login_required
def atender_turno(request):
    if cola_turnos:
        turno_id = cola_turnos.popleft()
        turno = Turno.objects.get(id=turno_id)
        turno.estado = 'atendido'
        turno.save()
        registrar_accion(request.user, f"Atendió a {turno.usuario.username}")
    return redirect('ver_turnos')

@login_required
def ver_turnos(request):
    turnos = Turno.objects.all().order_by('-hora_ingreso')
    return render(request, 'turnos.html', {'turnos': turnos})

def registrar_accion(usuario, descripcion):
    HistorialAccion.objects.create(usuario=usuario, accion=descripcion)
    pila_historial.append(descripcion)

@login_required
def deshacer_ultima_accion(request):
    if pila_historial:
        ultima = pila_historial.pop()
        HistorialAccion.objects.filter(usuario=request.user, accion=ultima).last().delete()
    return redirect('ver_historial')

@login_required
def ver_historial(request):
    historial = HistorialAccion.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'historial.html', {'historial': historial})
