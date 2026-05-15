from django.urls import path
from . import views
from .views import freshservice_proxy

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.inicio_view, name='inicio'),
    path('registrovictimas/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('equipo/', views.equipo_view, name='equipo'),
    path('contacto/', views.contacto_view, name='contacto'),
    path("ticket/", views.enviar_ticket, name="enviar_ticket"),
    path("mesa-ayuda/", freshservice_proxy, name="mesa_ayuda"),
    path('chatbot/', views.chatbot_ajax, name='chatbot_ajax'),
]