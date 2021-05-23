from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profil(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,verbose_name="Kullanıcı",null=True)
    profil=models.ImageField(upload_to="profil_resim/",verbose_name="Profil resmi")