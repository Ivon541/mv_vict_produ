from django.urls import path
from . import views

urlpatterns = [
    path('ticket/', views.crear_ticket, name='crear_ticket'),
    path('exito/', views.ticket_exito, name='ticket_exito'),
    path('tickets/', views.lista_tickets, name='lista_tickets'),
    path('kpi/', views.kpi, name='kpi'),
    path('faq/', views.faq, name='faq'),
]