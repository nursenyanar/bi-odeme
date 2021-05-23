"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from .views import *





urlpatterns = [
    path("masalar/",kayitlar,name="kayitlar"),
    path("z-raporu/",z_raporu,name="z_raporu"),
    path("masalar/masa/<int:masa_no>",masa_kaydi,name="masa_kaydi"),
    path("z-raporu/<int:masa_no>",z_rapor_kaydi,name="z_rapor_kaydi"),
    path("gunluk-z-raporu/",gunluk_z_raporu,name="gunluk_z_raporu"),
]

