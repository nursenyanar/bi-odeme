# Generated by Django 2.1.7 on 2020-08-26 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_auto_20200825_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='masa',
            name='toplam_ucret',
            field=models.FloatField(default=0, verbose_name='Toplam ücret'),
            preserve_default=False,
        ),
    ]
