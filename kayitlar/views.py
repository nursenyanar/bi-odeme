import json5
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from home.models import SiparisKayitlari, Masa
from kullanici.models import Profil
from menu.models import Menu
import datetime


@login_required(login_url="/login/")
def kayitlar(request):
    masalar = Masa.objects.all()
    user = Profil.objects.filter(user=request.user)
    bilgiler=[]
    if user:
        bilgiler = user[0]

    context = {
        "masa": masalar,
        "bilgi": bilgiler,
        "link": "/kayitlar/masalar/masa/",
        "title": "Geçmiş Masa Kayıtları"

    }
    return render(request, "gecmis_kayitlar.html", context)


@login_required(login_url="/login/")
def z_raporu(request):
    masalar = Masa.objects.all()
    user = Profil.objects.filter(user=request.user)
    bilgiler=[]
    if user:
        bilgiler = user[0]

    context = {
        "masa": masalar,
        "bilgi": bilgiler,
        "link": "/kayitlar/z-raporu/",
        "title": "Z Raporu"
    }
    return render(request, "gecmis_kayitlar.html", context)

@login_required(login_url="/login/")
def z_rapor_kaydi(request, masa_no):
    masa = Masa.objects.get(masa_no=masa_no)
    kayilar = SiparisKayitlari.objects.filter(masa_no=masa_no, siparis_zamani__day=timezone.now().day,siparis_zamani__month=timezone.now().month,siparis_zamani__year=timezone.now().year)
    menu = Menu.objects.all()
    bilgiler=[]
    user = Profil.objects.filter(user=request.user)

    if user:
        bilgiler = user[0]
    context = {
        "masa": masa,
        "kayitlar": kayilar,
        "menu": menu,
        "bilgi": bilgiler
    }

    list = {}
    tum_list={}
    toplam_para=0
    toplam_musteri=0
    for i in kayilar:
        toplam_para+=i.toplam_ucret
        toplam_musteri+=i.kisi_sayisi
        kayit = json5.loads(i.siparis_list)
        for k in kayit.keys():
            for m in menu:
                if int(k) == m.id:
                    if not m.urun_adi in list:
                        list[m.urun_adi] = [kayit[k], m.fiyat]
                    else:
                        temp = list.get(m.urun_adi)
                        list[m.urun_adi] = [temp[0] + kayit[k], m.fiyat]

    toplam_urun=0

    for i in list:
        sayi=list[i][0]
        toplam_urun+=sayi
        fiyat=list[i][1]
        tum_list[i]=[sayi,sayi*fiyat]

    context["list"]=tum_list
    context["toplam_para"]=toplam_para
    context["toplam_urun"]=toplam_urun
    context["toplam_musteri"]=toplam_musteri
    return render(request, "z-rapor-view.html", context)


@login_required(login_url="/login/")
def gunluk_z_raporu(request):
    kayilar = SiparisKayitlari.objects.filter(siparis_zamani__day=timezone.now().day)
    menu = Menu.objects.all()
    bilgiler=[]
    user = Profil.objects.filter(user=request.user)

    if user:
        bilgiler = user[0]
    context = {
        "kayitlar": kayilar,
        "menu": menu,
        "bilgi": bilgiler
    }

    list = {}
    tum_list={}
    toplam_para=0
    toplam_musteri=0
    for i in kayilar:
        toplam_para+=i.toplam_ucret
        toplam_musteri+=i.kisi_sayisi
        kayit = json5.loads(i.siparis_list)
        for k in kayit.keys():
            for m in menu:
                if int(k) == m.id:
                    if not m.urun_adi in list:
                        list[m.urun_adi] = [kayit[k], m.fiyat]
                    else:
                        temp = list.get(m.urun_adi)
                        list[m.urun_adi] = [temp[0] + kayit[k], m.fiyat]

    toplam_urun=0

    for i in list:
        sayi=list[i][0]
        toplam_urun+=sayi
        fiyat=list[i][1]
        tum_list[i]=[sayi,sayi*fiyat]

    context["list"]=tum_list
    context["toplam_para"]=toplam_para
    context["toplam_urun"]=toplam_urun
    context["toplam_musteri"]=toplam_musteri
    return render(request,"gunluk-z-raporu.html",context)


@login_required(login_url="/login/")
def masa_kaydi(request, masa_no):
    masa = Masa.objects.get(masa_no=masa_no)
    menu = Menu.objects.all()
    user = Profil.objects.filter(user=request.user)
    bilgiler=[]
    if user:
        bilgiler = user[0]
    context = {
        "masa": masa,
        "menu": menu,
        "bilgi": bilgiler
    }

    if request.GET.get("filtreleme_turu", None) == "basic":
        tur = request.GET.get("tur", None)
        if tur == "Günlük":
            kayitlar = SiparisKayitlari.objects.filter(masa_no=masa_no,
                                                       siparis_zamani__day=timezone.now().day,
                                                       siparis_zamani__month=timezone.now().month,
                                                       siparis_zamani__year=timezone.now().year).order_by("-id")
        elif tur == "Haftalık":
            one_week_ago = timezone.now().today() - timezone.timedelta(days=7)
            kayitlar = SiparisKayitlari.objects.filter(masa_no=masa_no, siparis_zamani__gte=one_week_ago,siparis_zamani__month=timezone.now().month,siparis_zamani__year=timezone.now().year).order_by(
                "-id")
        elif tur == "Aylık":
            kayitlar = SiparisKayitlari.objects.filter(masa_no=masa_no,
                                                       siparis_zamani__month=timezone.now().month,siparis_zamani__year=timezone.now().year).order_by("-id")
        else:
            kayitlar = SiparisKayitlari.objects.filter(masa_no=masa_no).order_by("-id")
        context["kayitlar"] = kayitlar

    elif request.GET.get("filtreleme_turu", None) == "belirli":
        tarih = request.GET.get("tarih", None)
        date = datetime.datetime.strptime(tarih, '%Y-%m-%d')

        kayitlar = SiparisKayitlari.objects.filter(masa_no=masa_no, siparis_zamani__day=date.day,siparis_zamani__month=timezone.now().month,siparis_zamani__year=timezone.now().year).order_by("-id")
        context["kayitlar"] = kayitlar

    elif request.GET.get("filtreleme_turu", None) == "aralık":
        baslangic = request.GET.get("baslangic", None)
        bitis = request.GET.get("bitis", None)

        date_baslangic = datetime.datetime.strptime(baslangic, '%Y-%m-%d')
        date_bitis = datetime.datetime.strptime(bitis, '%Y-%m-%d') + timezone.timedelta(days=1)

        kayitlar = SiparisKayitlari.objects.filter(masa_no=masa_no, siparis_zamani__gte=date_baslangic,
                                                   siparis_zamani__lte=date_bitis).order_by("-id")
        context["kayitlar"] = kayitlar

    else:
        kayitlar = SiparisKayitlari.objects.filter(masa_no=masa_no).order_by("-id")
        context["kayitlar"] = kayitlar

    return render(request, "masa_kayit_view.html", context)
