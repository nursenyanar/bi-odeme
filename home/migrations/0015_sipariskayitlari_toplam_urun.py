# Generated by Django 2.1.7 on 2020-08-23 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_sipariskayitlari_toplam_ucret'),
    ]

    operations = [
        migrations.AddField(
            model_name='sipariskayitlari',
            name='toplam_urun',
            field=models.FloatField(default=1, verbose_name='Toplam urun'),
            preserve_default=False,
        ),
    ]
