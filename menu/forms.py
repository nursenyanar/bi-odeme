from django import forms
from .models import *

class MenuEkleForm(forms.ModelForm):
    class Meta:
        model=Menu
        fields=[
            "urun_adi",
            "kategori",
            "porsiyon_1",
            "porsiyon_2",
            "porsiyon_1_5",
            "porsiyon_0_5",
            "resim",
            "aciklama"
        ]

    urun_adi=forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "type":"text",
                "class":"form-control form-control-user",
                "placeholder":"Ürün Adı",
            }
        )
    )

    kategori=forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "type":"text",
                "class":"form-control form-control-user",
                "placeholder":"Kategori",
                "list":"kategori"
            }
        )
    )

    porsiyon_1=forms.CharField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                "type":"number",
                "class":"form-control form-control-user",
                "placeholder":"Bir Porsiyon fiyatı",
                "step" :"0.01"
            }
        )
    )
    porsiyon_0_5=forms.CharField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                "type":"number",
                "class":"form-control form-control-user",
                "placeholder":"Yarım Porsiyon fiyatı",
                "step" :"0.01"
            }
        )
    )

    porsiyon_2=forms.CharField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                "type":"number",
                "class":"form-control form-control-user",
                "placeholder":"İki Porsiyon fiyatı",
                "step" :"0.01"
            }
        )
    )


    porsiyon_1_5=forms.CharField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                "type":"number",
                "class":"form-control form-control-user",
                "placeholder":"Bir Buçuk Porsiyon fiyatı",
                "step" :"0.01"
            }
        )
    )

    resim=forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "type":"file",
                "placeholder":"resim",
            }
        )
    )

    aciklama=forms.CharField(
        widget=forms.Textarea(
            attrs={
                "type":"text",
                "rows":"3",
                "class":"form-control form-control-user",
                "placeholder":"Açıklama",
            }
        )
    )