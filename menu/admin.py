from django.contrib import admin
from .models import *

# Register your models here.
class AdminKategori(admin.ModelAdmin):
    list_display = [
        "kategori"
    ]


class AdminMenu(admin.ModelAdmin):
    list_display = [
        "urun_adi",
        "porsiyon_1",
        "kategori",
        "ekleyen"
    ]


admin.site.register(Kategori, AdminKategori)
admin.site.register(Menu, AdminMenu)
