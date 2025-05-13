"""
URL configuration for victima_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from victima_app import views

router = routers.DefaultRouter()
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'contratos', views.ContratosViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('aut_app.urls')),
    path('victima/', include('victima_app.urls')),
    path('api-aut/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-victima/', include(router.urls)),
]
