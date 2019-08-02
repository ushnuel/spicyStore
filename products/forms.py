from django import forms
from . import models

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ('title','price','category','description','image')
