# Generated by Django 2.1.7 on 2020-08-23 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20200822_0357'),
    ]

    operations = [
        migrations.AddField(
            model_name='sipariskayitlari',
            name='toplam_ucret',
            field=models.FloatField(default=1, verbose_name='Toplam ücret'),
            preserve_default=False,
        ),
    ]
