from django.contrib.auth.models import User
from django.db import models
import uuid

# Create your models here.


class Masa(models.Model):
    masa_no=models.IntegerField(verbose_name="Masa numarası")
    masa_bosmu=models.BooleanField(verbose_name="Masa boşmu")
    siparis_list=models.TextField(verbose_name="Sipariş Listesi")
    kisi_say=models.IntegerField(verbose_name="Kisi Say",null=True,blank=True)
    toplam_ucret=models.FloatField(verbose_name="Toplam ücret")


class Siparis(models.Model):
    masa_no=models.IntegerField(verbose_name="masa no")
    siparis_list=models.TextField(verbose_name="Sipariş Listesi")
    kisi_say=models.IntegerField(verbose_name="Kisi Say",default=1)
    toplam_ucret=models.FloatField(verbose_name="Toplam ücret")

class SiparisKayitlari(models.Model):
    siparis_kayit=models.IntegerField(verbose_name="Sipariş id",null=True,blank=True)
    masa_no=models.IntegerField(verbose_name="Masa No")
    siparis_list=models.TextField(verbose_name="Siparis Listesi")
    siparis_zamani=models.DateTimeField(auto_now_add=True)
    kisi_sayisi=models.IntegerField(verbose_name="Kişi Sayısı",default=1)
    toplam_ucret=models.FloatField(verbose_name="Toplam ücret")
    toplam_urun=models.FloatField(verbose_name="Toplam urun")
    siparis_kapanis=models.DateTimeField(verbose_name="Kapanış saati",null=True,blank=True)


