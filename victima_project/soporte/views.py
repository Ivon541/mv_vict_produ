from django.shortcuts import render, redirect
from .models import Ticket, FAQ
from .forms import TicketForm


def crear_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ticket_exito')
    else:
        form = TicketForm()

    return render(request, 'soporte/crear_ticket.html', {'form': form})


def ticket_exito(request):
    return render(request, 'soporte/exito.html')


def lista_tickets(request):
    tickets = Ticket.objects.all().order_by('-fecha_creacion')
    return render(request, 'soporte/lista_tickets.html', {'tickets': tickets})


def kpi(request):
    total = Ticket.objects.count()
    resueltos = Ticket.objects.filter(estado='resuelto').count()
    porcentaje = (resueltos / total * 100) if total > 0 else 0

    return render(request, 'soporte/kpi.html', {
        'total': total,
        'resueltos': resueltos,
        'porcentaje': porcentaje
    })


def faq(request):
    faqs = FAQ.objects.all()
    return render(request, 'soporte/faq.html', {'faqs': faqs})