from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import logout
from django.contrib.auth.models import User  # Importar el modelo User
import requests
from django.conf import settings
from django.shortcuts import render
from .forms import TicketForm
import requests
from django.http import HttpResponse
import json
from django.http import JsonResponse
from .services import consultar_chatbot_victimas
from .services import PREGUNTAS_FRECUENTES

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("dashboard"))
        return render(request, "aut_app/login.html", {"error": "Invalid username or password"})
    return render(request, "aut_app/login.html")

def inicio_view(request):
    return render(request, "aut_app/home.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        superusuario = 0
        equipo_trabajo = 0
        activo = 1
        
        if request.POST.get("password1") != request.POST.get("password2"):
            return render(request, "aut_app/register.html", {"error": "Passwords do not match"})
        if User.objects.filter(username=username).exists():
            return render(request, "aut_app/register.html", {"error": "Username already exists"})
        if User.objects.filter(email=email).exists():
            return render(request, "aut_app/register.html", {"error": "Email already exists"})
        password = request.POST.get("password1")

        # Verificar si la contraseña contiene caracteres especiales
        if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in password):
            return render(request, "aut_app/register.html", {"error": "Password must contain at least one special character"})
        
        # Verificar la fortaleza de la contraseña
        if password.islower() or password.isupper():
            return render(request, "aut_app/register.html", {"error": "Password must contain both uppercase and lowercase letters"})
        if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in password):
            return render(request, "aut_app/register.html", {"error": "Password must contain at least one special character"})
        if len(password) < 8:
            return render(request, "aut_app/register.html", {"error": "Password must be at least 8 characters long"})
        if not any(char.isdigit() for char in password):
            return render(request, "aut_app/register.html", {"error": "Password must contain at least one number"})
        if not any(char.isalpha() for char in password):
            return render(request, "aut_app/register.html", {"error": "Password must contain at least one letter"})

        # Verificar el formato del correo electrónico
        try:
            validate_email(email)
        except ValidationError:
            return render(request, "aut_app/register.html", {"error": "Invalid email format"})
        # Crear el usuario en la base de datos        
        User.objects.create_user(username=username, email=email, password=password, first_name=firstname, last_name=lastname, is_superuser=superusuario, is_active=activo, is_staff=equipo_trabajo)  # Crear un nuevo usuario
        return HttpResponseRedirect(reverse("login"))  # Redirigir a la página de inicio de sesión después del registro
    return render(request, "aut_app/register.html")

def logout_view(request):
    logout(request)
    return render(request, "aut_app/logout.html")
    
def dashboard_view(request):
    if request.user.is_authenticated:
        return render(request, "aut_app/dashboard.html")
    else:
        return HttpResponseRedirect(reverse("login"))
    
def equipo_view(request):
    return render(request, "aut_app/equipo.html")


def contacto_view(request):
    return render(request, "aut_app/contacto.html")
    

# aut_app/views.py


def enviar_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():

            nombre = form.cleaned_data["nombre"]
            email = form.cleaned_data["email"]
            asunto = form.cleaned_data["asunto"]
            mensaje = form.cleaned_data["mensaje"]

            # URL de tu Freshdesk
            url = "https://soportevictimas.freshdesk.com/api/v2/tickets"

            payload = {
                "email": email,
                "subject": asunto,
                "description": f"Nombre: {nombre}\n\nMensaje:\n{mensaje}",
                "priority": 1,
                "status": 2
            }

            # API KEY (debes poner la tuya)
            api_key = "TU_API_KEY_DE_FRESHDESK"

            response = requests.post(
                url,
                auth=(api_key, "X"),
                json=payload
            )

            if response.status_code == 201:
                return render(request, "ticket_exito.html")
            else:
                return render(request, "ticket_error.html", {
                    "codigo": response.status_code,
                    "error": response.text
                })

    else:
        form = TicketForm()

    return render(request, "ticket_form.html", {"form": form})
    if request.method == "POST":
        form = TicketForm(request.POST)

        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            documento = form.cleaned_data["documento"]
            correo = form.cleaned_data["correo"]
            asunto = form.cleaned_data["asunto"]
            prioridad = form.cleaned_data["prioridad"]
            descripcion = form.cleaned_data["descripcion"]

            # ========== CONFIGURACIÓN FRESHDESK ==========
            freshdesk_url = "https://soportevictimas.freshdesk.com/api/v2/tickets"
            api_key = "Xe6h1TBM3dM_MOicV34N"   # Cambia por la tuya

            headers = {
                "Content-Type": "application/json"
            }

            payload = {
                "email": correo,
                "subject": asunto,
                "description": (
                    f"Nombre: {nombre}\n"
                    f"Documento: {documento}\n\n"
                    f"Descripción del caso:\n{descripcion}"
                ),
                "priority": int(prioridad),
                "status": 2
            }

            # ====== ENVÍO DEL TICKET ======
            response = requests.post(
                freshdesk_url,
                auth=(api_key, "Xe6h1TBM3dM_MOicV34N"),  # API KEY + X obligatorio en Freshdesk
                headers=headers,
                json=payload
            )

            # ====== RESPUESTA DEL SERVIDOR ======
            if response.status_code == 201:
                messages.success(request, "🎉 Ticket creado y enviado al Help Desk correctamente.")
            else:
                messages.error(request, "❌ Error enviando el ticket al Help Desk.")
                print("ERROR FRESHDESK:", response.text)

            return redirect("crear_ticket")

    else:
        form = TicketForm()

    return render(request, "aut_app/soporte.html", {"form": form})

# views.py


def freshservice_proxy(request):
    url = "https://infovictimas.freshservice.com/support/home"

    # Hacemos la petición desde tu backend
    response = requests.get(url)

    # Devolvemos el HTML tal cual
    return HttpResponse(response.text)



from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from .services import (
    consultar_chatbot_victimas,
    PREGUNTAS_FRECUENTES
)


@csrf_exempt
def chatbot_ajax(request):

    if request.method == "POST":

        try:

            data = json.loads(request.body)

            pregunta = data.get(
                "pregunta",
                ""
            ).strip()

            if not pregunta:
                return JsonResponse({
                    "respuesta":
                    "Escribe una pregunta."
                })

            historial = request.session.get(
                "historial_chat",
                []
            )

            respuesta = consultar_chatbot_victimas(
                pregunta,
                historial
            )

            historial.append({
                "usuario": pregunta,
                "bot": respuesta
            })

            historial = historial[-10:]

            request.session[
                "historial_chat"
            ] = historial

            return JsonResponse({
                "respuesta": respuesta
            })

        except Exception as e:

            print("ERROR CHATBOT:", e)

            return JsonResponse({
                "respuesta":
                "Error del servidor."
            })

    return JsonResponse({
        "respuesta":
        "Método no permitido."
    })