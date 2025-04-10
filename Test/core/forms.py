from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import ContactMessage

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': "••••••••"
    }))

class SignupForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address'"e.g. example@mail.com",
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': "e.g. John Doe",
            'class': 'w-full py-4 px-6 rounded-xl'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': "••••••••",
            'class': 'w-full py-4 px-6 rounded-xl'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': "••••••••",
            'class': 'w-full py-4 px-6 rounded-xl'
        })

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'class' :'w-full py-4 px-6 rounded-xl'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email',
                'class' :'w-full py-4 px-6 rounded-xl'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message',
                'rows': 5,
                'class' :'w-full py-4 px-6 rounded-xl'
            }),
        }
