from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import ContactMessage, Review, UserProfile

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

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address'"e.g. example@mail.com",
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'form-control',
                'placeholder': 'Rating (1-5)'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your review here...',
                'rows': 4
            })
        }

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Tell us about yourself...',
        'rows': 4
    }))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phone Number'
    }))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Address'
    }))
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = UserProfile
        fields = ['photo', 'bio', 'phone', 'address']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
