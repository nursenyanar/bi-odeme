# Generated by Django 2.1.7 on 2020-09-02 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0007_auto_20200819_2031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='fiyat',
        ),
        migrations.AddField(
            model_name='menu',
            name='porsiyon_0_5',
            field=models.FloatField(default=1, verbose_name='Yarım Porsiyon Fiyat'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menu',
            name='porsiyon_1',
            field=models.FloatField(default=1, verbose_name='Bir Porsiyon Fiyat'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menu',
            name='porsiyon_1_5',
            field=models.FloatField(default=1, verbose_name='Bir Buçuk Porsiyon Fiyat'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menu',
            name='porsiyon_2',
            field=models.FloatField(default=1, verbose_name='İki Porsiyon Fiyat'),
            preserve_default=False,
        ),
    ]