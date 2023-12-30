from django import forms
from .models import Ad


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'img_url', 'link', 'unique_id_ad', 'advertiser']
