from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import logout
from django.contrib.auth.models import User  # Importar el modelo User

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("inicio"))
        else:
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
