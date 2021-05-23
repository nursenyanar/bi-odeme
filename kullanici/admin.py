from django.contrib import admin
from .models import *


# Register your models here.

class AdminProfil(admin.ModelAdmin):
    list_display = ["user"]


admin.site.register(Profil, AdminProfil)
