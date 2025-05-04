from django import forms
from items.models import Items
from django.forms import ClearableFileInput

class ItemForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ['category', 'name', 'price', 'description', 'image', 'quantity', 'for_sale', 'advertise', 'quantity_advertise']
        widgets = {
            'image': forms.FileInput(),  # Use simple FileInput instead of ClearableFileInput
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the clear checkbox label completely
        self.fields['image'].widget.clear_checkbox_label = ''
        self.fields['image'].widget.template_name = 'django/forms/widgets/file.html'
class YourItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.clear_checkbox_label = ''
        self.fields['image'].widget.template_name = 'django/forms/widgets/clearable_file_input.html'
        self.fields['image'].widget.attrs.update({'class': 'hidden-file-input'})
class CustomClearableFileInput(ClearableFileInput):
    template_name = 'widgets/custom_clearable_file_input.html'
    initial_text = ''
    input_text = ''
    clear_checkbox_label = ''