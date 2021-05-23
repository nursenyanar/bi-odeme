from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class ProfilModel(models.ForeignKey):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    profil_image=models.FileField(upload_to="profil/",verbose_name="Profil")