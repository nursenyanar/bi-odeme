from django.contrib.auth.models import User
from django.db import models
from sorl.thumbnail import ImageField, get_thumbnail

# Create your models here.
class Kategori(models.Model):
    kategori=models.CharField(max_length=250,verbose_name="Kategori")


class Menu(models.Model):
    urun_adi=models.CharField(max_length=250,verbose_name="Ürün Adı")
    porsiyon_1=models.FloatField(verbose_name="Bir Porsiyon Fiyat",null=True,blank=True)
    porsiyon_2=models.FloatField(verbose_name="İki Porsiyon Fiyat",null=True,blank=True)
    porsiyon_1_5=models.FloatField(verbose_name="Bir Buçuk Porsiyon Fiyat",null=True,blank=True)
    porsiyon_0_5=models.FloatField(verbose_name="Yarım Porsiyon Fiyat",null=True,blank=True)
    kategori=models.CharField(verbose_name="Kategori",max_length=250)
    ekleyen=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    resim=ImageField(upload_to="menu-resim/",verbose_name="Resim",null=True)
    aciklama=models.TextField(verbose_name="Açıklama")

