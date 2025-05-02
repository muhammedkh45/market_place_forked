from django import forms
from items.models import Items
class ItemForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ['category', 'name', 'price', 'description', 'image', 'quantity', 'for_sale', 'advertise', 'quantity_advertise']