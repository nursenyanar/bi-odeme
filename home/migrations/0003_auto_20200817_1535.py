# Generated by Django 2.1.7 on 2020-08-17 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20200817_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='kategori',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kategori_adi', to='home.Kategori'),
        ),
    ]
