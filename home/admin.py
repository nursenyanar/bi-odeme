from django.contrib import admin
from .models import *


# Register your models here.


class AdminModel(admin.ModelAdmin):
    list_display = [
        "masa_no",
        "masa_bosmu",
        "siparis_list"
    ]


class AdminSiparisKaydi(admin.ModelAdmin):
    list_display = [
        "masa_no",
        "siparis_list",
        "siparis_zamani",
        "kisi_sayisi"
    ]


admin.site.register(Masa, AdminModel)
admin.site.register(SiparisKayitlari, AdminSiparisKaydi)
