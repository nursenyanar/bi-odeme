from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from home.models import *
from kullanici.models import Profil
from menu.models import Kategori, Menu
import json5
from django.db.models import Avg
from django.utils import timezone
import datetime
import random


@login_required(login_url="/login/")
def index(request):
    user = Profil.objects.filter(user=request.user)
    bilgiler=[]
    if user:
        bilgiler = user[0]
    musteri_bilgileri = musteri_ortalama_getir()
    haftalik_bilgileri=ortalama_haftalik_kazanc()
    haftalik_satilan_urun=haftalik_satilan_urun_sayisi()

    context = {
        "msg": "deneme",
        "bilgi": bilgiler,
        "liste": musteri_bilgileri[0],
        "ortalama_musteri": musteri_bilgileri[2],
        "gun_adlari": musteri_bilgileri[1][::-1],
        "haftalik_kazanc_list":haftalik_bilgileri[0],
        "ortalama_para":haftalik_bilgileri[1],
        "satilan_urun_list":haftalik_satilan_urun[0],
        "satilan_toplam_urun":haftalik_satilan_urun[1],
        "gecen_hafta":musteri_karsilastir(),
        "bu_hafta":bu_hafta_musteri_karsilastir(),
        "gecen_hafta_para":gecen_hafta_para_karsilastir(),
        "bu_hafta_para":bu_hafta_para_karsilastir()
    }
    return render(request, "index.html", context)


@login_required(login_url="/login/")
def siparis(request):
    kontrol = Masa.objects.all()
    if len(kontrol) == 0:
        for i in range(1, 51):
            Masa.objects.create(masa_no=i, masa_bosmu=True)
    masa = Masa.objects.all()
    user = Profil.objects.filter(user=request.user)
    bilgiler=[]
    if user:
        bilgiler = user[0]
    masa_kontrol = request.session.get("kontrol")
    context = {
        "masa": masa,
        "bilgi": bilgiler,
        "kontrol": masa_kontrol
    }
    request.session["kontrol"] = False
    return render(request, "siparis.html", context)


@login_required(login_url="/login/")
def siparis_goruntule(request, masa):

    masa_tasi=request.GET.get("masa_no",None)

    if masa_tasi:
        masa_bilgileri=Masa.objects.get(masa_no=masa)
        Masa.objects.filter(masa_no=masa_tasi).update(masa_bosmu=False,siparis_list=masa_bilgileri.siparis_list,kisi_say=masa_bilgileri.kisi_say,toplam_ucret=masa_bilgileri.toplam_ucret)
        Masa.objects.filter(masa_no=masa).update(masa_bosmu=True,siparis_list="{}",kisi_say=0,toplam_ucret=0)
        siparis_kayit=Siparis.objects.get(masa_no=masa)
        SiparisKayitlari.objects.filter(siparis_kayit=siparis_kayit.id).update(masa_no=masa_tasi)
        Siparis.objects.filter(masa_no=masa).update(masa_no=masa_tasi)
        return redirect("siparis")

    if request.method == "POST":
        veri = request.POST.get("veri")
        kisi_say = request.POST.get("kisi_say")
        siparis_update_or_create(veri, kisi_say,masa)
        return redirect(request.META.get('HTTP_REFERER'))
    user = Profil.objects.filter(user=request.user)
    bilgiler=[]
    if user:
        bilgiler = user[0]
    masa_bilgiler = Masa.objects.get(masa_no=masa)
    kategori = Kategori.objects.all()
    menu = Menu.objects.all()
    tum_masalar=Masa.objects.all()
    context = {
        "masa": masa_bilgiler,
        "bilgi": bilgiler,
        "kategoriler": kategori,
        "menu": menu,
        "tum_masalar":tum_masalar
    }
    return render(request, "masa_goruntule.html", context)


@login_required(login_url="/login/")
def hesap_al(request, masa):
    user = Profil.objects.filter(user=request.user)
    bilgiler=[]
    if user:
        bilgiler = user[0]
    masa_bilgileri = Masa.objects.get(masa_no=masa)
    menu = Menu.objects.all()

    if request.method == "POST":
        Masa.objects.filter(masa_no=masa).update(masa_bosmu=True, siparis_list="{}", kisi_say=0)
        kayit = Siparis.objects.filter(masa_no=masa)
        print(kayit[0].siparis_list,kayit[0].id)
        SiparisKayitlari.objects.filter(siparis_kayit=kayit[0].id).update(siparis_kapanis=timezone.now())
        kayit.delete()
        request.session["kontrol"] = True
        return redirect("siparis")
    context = {
        "menu": menu,
        "masa": masa_bilgileri,
        "bilgi": bilgiler
    }
    return render(request, "hesap-al.html", context)


@login_required(login_url="/login/")
def ara_toplam(request):
    if request.method == "POST":
        new_list = {
            "siparisler":[]
        }
        veri = request.POST.get("veri")
        masa = request.POST.get("masa")
        json = json5.loads(veri)
        toplam=0
        for i in json["siparisler"]:
            if i["adet"] > 0:
                toplam+=i["adet"]*i["fiyat"]
                new_list["siparisler"].append(i)
        if len(new_list["siparisler"]):
            Masa.objects.filter(masa_no=masa).update(masa_bosmu=False, siparis_list=new_list,toplam_ucret=toplam)
        else:
            kayit=Siparis.objects.filter(masa_no=masa)
            SiparisKayitlari.objects.filter(siparis_kayit=kayit[0].id).update(siparis_kapanis=timezone.now())
            kayit.delete()
            Masa.objects.filter(masa_no=masa).update(masa_bosmu=True, siparis_list=new_list, kisi_say=0)
            request.session["kontrol"] = True
            return redirect("siparis")
    return redirect(request.META.get('HTTP_REFERER'))


def musteri_ortalama_getir():
    ingilizce_gunler = {
        "Monday": "Pazartesi",
        "Tuesday": "Salı",
        "Wednesday": "Çarşamba",
        "Thursday": "Perşembe",
        "Friday": "Cuma",
        "Saturday": "Cumartesi",
        "Sunday": "Pazar"
    }
    gun_1=timezone.now().today()-datetime.timedelta(days=1)
    gun_2=timezone.now().today()-datetime.timedelta(days=2)
    gun_3=timezone.now().today()-datetime.timedelta(days=3)
    gun_4=timezone.now().today()-datetime.timedelta(days=4)
    gun_5=timezone.now().today()-datetime.timedelta(days=5)
    gun_6=timezone.now().today()-datetime.timedelta(days=6)
    gun_7=timezone.now().today()-datetime.timedelta(days=7)

    gun_once_7 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_7.strftime('%d')
                                                 ,siparis_zamani__month=gun_7.strftime('%m')
                                                 ,siparis_zamani__year=gun_7.strftime('%Y'))
    gun_once_6 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_6.strftime('%d')
                                                 ,siparis_zamani__month=gun_6.strftime('%m')
                                                 ,siparis_zamani__year=gun_6.strftime('%Y'))
    gun_once_5 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_5.strftime('%d')
                                                 ,siparis_zamani__month=gun_5.strftime('%m')
                                                 ,siparis_zamani__year=gun_5.strftime('%Y'))
    gun_once_4 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_4.strftime('%d')
                                                 ,siparis_zamani__month=gun_4.strftime('%m')
                                                 ,siparis_zamani__year=gun_4.strftime('%Y'))
    gun_once_3 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_3.strftime('%d')
                                                 ,siparis_zamani__month=gun_3.strftime('%m')
                                                 ,siparis_zamani__year=gun_3.strftime('%Y'))
    gun_once_2 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_2.strftime('%d')
                                                 ,siparis_zamani__month=gun_2.strftime('%m')
                                                 ,siparis_zamani__year=gun_2.strftime('%Y'))
    gun_once_1 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_1.strftime('%d')
                                                 ,siparis_zamani__month=gun_1.strftime('%m')
                                                 ,siparis_zamani__year=gun_1.strftime('%Y'))
    gecici_list = [gun_once_7, gun_once_6, gun_once_5,
             gun_once_4, gun_once_3, gun_once_2,
             gun_once_1]

    for i in gecici_list:
        if i is None:
            gecici_list[gecici_list.index(i)] = 0
    list=[]
    for i in gecici_list:
        toplam=0
        for veri in i:
            toplam+=veri.kisi_sayisi
        list.append(toplam)


    gun_adlari = []
    for i in range(1, 7):
        zaman = timezone.now() - datetime.timedelta(days=i)
        gun_adi = zaman.strftime("%A")
        gun_adlari.append(ingilizce_gunler[gun_adi])
    gun_adi = timezone.now().strftime("%A")
    gun_adlari.append(ingilizce_gunler[gun_adi])

    haftalik_musteri = 0

    for i in list:
        haftalik_musteri += i

    return list, gun_adlari, haftalik_musteri

def ortalama_haftalik_kazanc():
    gun_1=timezone.now().today()-datetime.timedelta(days=1)
    gun_2=timezone.now().today()-datetime.timedelta(days=2)
    gun_3=timezone.now().today()-datetime.timedelta(days=3)
    gun_4=timezone.now().today()-datetime.timedelta(days=4)
    gun_5=timezone.now().today()-datetime.timedelta(days=5)
    gun_6=timezone.now().today()-datetime.timedelta(days=6)
    gun_7=timezone.now().today()-datetime.timedelta(days=7)

    gun_once_7 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_7.strftime('%d')
                                                 ,siparis_zamani__month=gun_7.strftime('%m')
                                                 ,siparis_zamani__year=gun_7.strftime('%Y'))
    gun_once_6 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_6.strftime('%d')
                                                 ,siparis_zamani__month=gun_6.strftime('%m')
                                                 ,siparis_zamani__year=gun_6.strftime('%Y'))
    gun_once_5 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_5.strftime('%d')
                                                 ,siparis_zamani__month=gun_5.strftime('%m')
                                                 ,siparis_zamani__year=gun_5.strftime('%Y'))
    gun_once_4 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_4.strftime('%d')
                                                 ,siparis_zamani__month=gun_4.strftime('%m')
                                                 ,siparis_zamani__year=gun_4.strftime('%Y'))
    gun_once_3 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_3.strftime('%d')
                                                 ,siparis_zamani__month=gun_3.strftime('%m')
                                                 ,siparis_zamani__year=gun_3.strftime('%Y'))
    gun_once_2 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_2.strftime('%d')
                                                 ,siparis_zamani__month=gun_2.strftime('%m')
                                                 ,siparis_zamani__year=gun_2.strftime('%Y'))
    gun_once_1 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_1.strftime('%d')
                                                 ,siparis_zamani__month=gun_1.strftime('%m')
                                                 ,siparis_zamani__year=gun_1.strftime('%Y'))
    gecici_list = [gun_once_7, gun_once_6, gun_once_5,
             gun_once_4, gun_once_3, gun_once_2,
             gun_once_1]

    for i in gecici_list:
        if i is None:
            gecici_list[gecici_list.index(i)] = 0
    list=[]
    for i in gecici_list:
        toplam=0
        for veri in i:
            toplam+=veri.toplam_ucret
        list.append(toplam)

    haftalık_kazanc = 0
    for i in list:
        haftalık_kazanc += i

    return list, int(haftalık_kazanc)

def haftalik_satilan_urun_sayisi():
    gun_1=timezone.now().today()-datetime.timedelta(days=1)
    gun_2=timezone.now().today()-datetime.timedelta(days=2)
    gun_3=timezone.now().today()-datetime.timedelta(days=3)
    gun_4=timezone.now().today()-datetime.timedelta(days=4)
    gun_5=timezone.now().today()-datetime.timedelta(days=5)
    gun_6=timezone.now().today()-datetime.timedelta(days=6)
    gun_7=timezone.now().today()-datetime.timedelta(days=7)

    gun_once_7 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_7.strftime('%d')
                                                 ,siparis_zamani__month=gun_7.strftime('%m')
                                                 ,siparis_zamani__year=gun_7.strftime('%Y'))
    gun_once_6 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_6.strftime('%d')
                                                 ,siparis_zamani__month=gun_6.strftime('%m')
                                                 ,siparis_zamani__year=gun_6.strftime('%Y'))
    gun_once_5 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_5.strftime('%d')
                                                 ,siparis_zamani__month=gun_5.strftime('%m')
                                                 ,siparis_zamani__year=gun_5.strftime('%Y'))
    gun_once_4 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_4.strftime('%d')
                                                 ,siparis_zamani__month=gun_4.strftime('%m')
                                                 ,siparis_zamani__year=gun_4.strftime('%Y'))
    gun_once_3 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_3.strftime('%d')
                                                 ,siparis_zamani__month=gun_3.strftime('%m')
                                                 ,siparis_zamani__year=gun_3.strftime('%Y'))
    gun_once_2 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_2.strftime('%d')
                                                 ,siparis_zamani__month=gun_2.strftime('%m')
                                                 ,siparis_zamani__year=gun_2.strftime('%Y'))
    gun_once_1 = SiparisKayitlari.objects.filter(
                                                 siparis_zamani__day=gun_1.strftime('%d')
                                                 ,siparis_zamani__month=gun_1.strftime('%m')
                                                 ,siparis_zamani__year=gun_1.strftime('%Y'))
    gecici_list = [gun_once_7, gun_once_6, gun_once_5,
             gun_once_4, gun_once_3, gun_once_2,
             gun_once_1]

    for i in gecici_list:
        if i is None:
            gecici_list[gecici_list.index(i)] = 0
    list=[]
    for i in gecici_list:
        toplam=0
        for veri in i:
            toplam+=veri.toplam_urun
        list.append(toplam)

    haftalık_kazanc = 0
    for i in list:
        haftalık_kazanc += i

    return list, haftalık_kazanc



@login_required(login_url="/login/")
def siparis_sil(request, masa):
    Masa.objects.filter(masa_no=masa).update(masa_bosmu=True, siparis_list="{}", kisi_say=0)
    siparis_kaydi = Siparis.objects.get(masa_no=masa)
    SiparisKayitlari.objects.filter(siparis_kayit=siparis_kaydi.id).delete()
    siparis_kaydi.delete()
    return redirect("siparis")


def siparis_update_or_create(veri, kisi_say,masa):
    toplam_ucret = 0
    toplam_adet=0
    data = json5.loads(veri)
    for i in data["siparisler"]:
        for j in i:
            if j=="adet":
                toplam_adet+=i["adet"]
            if j=="fiyat":
                toplam_ucret+=i["adet"]*i["fiyat"]

    if len(kisi_say) > 0:
        if int(kisi_say) < 1:
            kisi_say = 1
    else:
        kisi_say = 1
    Masa.objects.filter(masa_no=masa).update(masa_bosmu=False, siparis_list=veri, kisi_say=kisi_say,toplam_ucret=toplam_ucret)
    if Siparis.objects.filter(masa_no=masa):
        Siparis.objects.filter(masa_no=masa).update(siparis_list=veri, kisi_say=kisi_say,toplam_ucret=toplam_ucret)
    else:
        Siparis.objects.create(masa_no=masa, siparis_list=veri, kisi_say=kisi_say,toplam_ucret=toplam_ucret)
    kayit = Siparis.objects.get(masa_no=masa)
    if SiparisKayitlari.objects.filter(siparis_kayit=kayit.id):
        SiparisKayitlari.objects.filter(siparis_kayit=kayit.id).update(siparis_list=veri, kisi_sayisi=kisi_say,
                                                                       toplam_ucret=toplam_ucret,toplam_urun=toplam_adet)
    else:
        SiparisKayitlari.objects.create(siparis_kayit=kayit.id, masa_no=masa, siparis_list=veri,
                                        kisi_sayisi=kisi_say, toplam_ucret=toplam_ucret,toplam_urun=toplam_adet)


def musteri_karsilastir():
    today = datetime.date.today()
    pazartesi = today + datetime.timedelta(days=-today.weekday(), weeks=-1)

    bitis=pazartesi+timezone.timedelta(days=7)
    kayitlar=SiparisKayitlari.objects.filter(siparis_zamani__range=[pazartesi.strftime('%Y-%m-%d'),bitis.strftime('%Y-%m-%d')])

    pzt=0
    sl=0
    car=0
    per = 0
    cum=0
    cmr=0
    paz=0
    for i in kayitlar:
        if i.siparis_zamani.strftime("%A")=="Monday":
            pzt+=i.kisi_sayisi
        elif i.siparis_zamani.strftime("%A")=="Tuesday":
            sl+=i.kisi_sayisi
        elif i.siparis_zamani.strftime("%A")=="Wednesday":
            car+=i.kisi_sayisi
        elif i.siparis_zamani.strftime("%A")=="Thursday":
            per+=i.kisi_sayisi
        elif i.siparis_zamani.strftime("%A")=="Friday":
            cum+=i.kisi_sayisi
        elif i.siparis_zamani.strftime("%A")=="Saturday":
            cmr+=i.kisi_sayisi
        else:
            paz+=i.kisi_sayisi

    return [pzt,sl,car,per,cum,cmr,paz]


def bu_hafta_musteri_karsilastir():
    pzt=0
    sl=0
    car=0
    per = 0
    cum=0
    cmr=0
    paz=0
    today = datetime.date.today()
    if today.strftime("%A") == "Monday":
        pazartesi = today + datetime.timedelta(days=-today.weekday())
        kayit=SiparisKayitlari.objects.filter(siparis_zamani__day=today.day,siparis_zamani__month=today.month,siparis_zamani__year=today.year)
        for i in kayit:
            pzt+=i.kisi_sayisi
        return [pzt]
    else:
        pazartesi = today + datetime.timedelta(days=-today.weekday())
        kayitlar=SiparisKayitlari.objects.filter(siparis_zamani__range=[pazartesi.strftime('%Y-%m-%d'),timezone.now().today() + datetime.timedelta(days=1)])

    for i in kayitlar:
        if i.siparis_zamani.strftime("%A")=="Monday":
            pzt+=i.kisi_sayisi
        elif i.siparis_zamani.strftime("%A")=="Tuesday":
            sl+=i.kisi_sayisi
        elif i.siparis_zamani.strftime("%A")=="Wednesday":
            car+=i.kisi_sayisi
        elif i.siparis_zamani.strftime("%A")=="Thursday":
            per+=i.kisi_sayisi
        elif i.siparis_zamani.strftime("%A")=="Friday":
            cum+=i.kisi_sayisi
        elif i.siparis_zamani.strftime("%A")=="Saturday":
            cmr+=i.kisi_sayisi
        elif i.siparis_zamani.strftime("%A")=="Sunday":
            paz+=i.kisi_sayisi
    list=[]
    if timezone.now().strftime("%A")=="Monday":
        list=[pzt]
    elif timezone.now().strftime("%A")=="Tuesday":
        list=[pzt,sl]
    elif timezone.now().strftime("%A")=="Wednesday":
        list=[pzt,sl,car]
    elif timezone.now().strftime("%A")=="Thursday":
        list=[pzt,sl,car,per]
    elif timezone.now().strftime("%A")=="Friday":
        list=[pzt,sl,car,per,cum]
    elif timezone.now().strftime("%A")=="Saturday":
        list=[pzt,sl,car,per,cum,cmr]
    elif timezone.now().strftime("%A")=="Sunday":
        list=[pzt,sl,car,per,cum,cmr,paz]

    return list



def gecen_hafta_para_karsilastir():
    today = datetime.date.today()
    pazartesi = today + datetime.timedelta(days=-today.weekday(), weeks=-1)

    bitis=pazartesi+timezone.timedelta(days=7)
    kayitlar=SiparisKayitlari.objects.filter(siparis_zamani__range=[pazartesi.strftime('%Y-%m-%d'),bitis.strftime('%Y-%m-%d')])

    pzt=0
    sl=0
    car=0
    per = 0
    cum=0
    cmr=0
    paz=0
    for i in kayitlar:
        if i.siparis_zamani.strftime("%A")=="Monday":
            pzt+=i.toplam_ucret
        elif i.siparis_zamani.strftime("%A")=="Tuesday":
            sl+=i.toplam_ucret
        elif i.siparis_zamani.strftime("%A")=="Wednesday":
            car+=i.toplam_ucret
        elif i.siparis_zamani.strftime("%A")=="Thursday":
            per+=i.toplam_ucret
        elif i.siparis_zamani.strftime("%A")=="Friday":
            cum+=i.toplam_ucret
        elif i.siparis_zamani.strftime("%A")=="Saturday":
            cmr+=i.toplam_ucret
        else:
            paz+=i.toplam_ucret

    return [pzt,sl,car,per,cum,cmr,paz]


def bu_hafta_para_karsilastir():
    pzt=0
    sl=0
    car=0
    per = 0
    cum=0
    cmr=0
    paz=0
    today = datetime.date.today()
    if today.strftime("%A") == "Monday":
        pazartesi = today + datetime.timedelta(days=-today.weekday())
        kayit=SiparisKayitlari.objects.filter(siparis_zamani__day=today.day,siparis_zamani__month=today.month,siparis_zamani__year=today.year)
        for i in kayit:
            pzt+=i.toplam_ucret
        return [pzt]
    else:
        pazartesi = today + datetime.timedelta(days=-today.weekday())
        kayitlar=SiparisKayitlari.objects.filter(siparis_zamani__range=[pazartesi.strftime('%Y-%m-%d'),timezone.now().today() + datetime.timedelta(days=1)])

    for i in kayitlar:
        if i.siparis_zamani.strftime("%A")=="Monday":
            pzt+=i.toplam_ucret
        elif i.siparis_zamani.strftime("%A")=="Tuesday":
            sl+=i.toplam_ucret
        elif i.siparis_zamani.strftime("%A")=="Wednesday":
            car+=i.toplam_ucret
        elif i.siparis_zamani.strftime("%A")=="Thursday":
            per+=i.toplam_ucret
        elif i.siparis_zamani.strftime("%A")=="Friday":
            cum+=i.toplam_ucret
        elif i.siparis_zamani.strftime("%A")=="Saturday":
            cmr+=i.toplam_ucret
        elif i.siparis_zamani.strftime("%A")=="Sunday":
            paz+=i.toplam_ucret
    list=[]
    if timezone.now().strftime("%A")=="Monday":
        list=[pzt]
    elif timezone.now().strftime("%A")=="Tuesday":
        list=[pzt,sl]
    elif timezone.now().strftime("%A")=="Wednesday":
        list=[pzt,sl,car]
    elif timezone.now().strftime("%A")=="Thursday":
        list=[pzt,sl,car,per]
    elif timezone.now().strftime("%A")=="Friday":
        list=[pzt,sl,car,per,cum]
    elif timezone.now().strftime("%A")=="Saturday":
        list=[pzt,sl,car,per,cum,cmr]
    elif timezone.now().strftime("%A")=="Sunday":
        list=[pzt,sl,car,per,cum,cmr,paz]
    return list

