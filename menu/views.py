from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from kullanici.models import Profil
from .forms import *



@login_required(login_url="/login/")
def tum_menu(request):
    bilgiler=[]
    kategoriler=Kategori.objects.all()
    menu=Menu.objects.all()

    for i in menu:
        print(i.urun_adi)
    context={
        "menu":menu,
        "kategori":kategoriler,
    }
    if request.user.is_authenticated:
        user=Profil.objects.filter(user=request.user)
        if user:
            bilgiler=user[0]
            context["bilgi"]=bilgiler
    return render(request,"tum-menu.html",context)

