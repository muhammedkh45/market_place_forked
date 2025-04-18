from django.urls import path
from django.contrib.auth import views as auth_views
from . import views,forms

urlpatterns = [
    path('',views.index,name='Index'),
    path('about',views.about,name="About"),
    path('contactus',views.contactus,name='ContactUs'),
    path('terms',views.terms,name='TermsandPolicy'),
    path('signup',views.signup,name='signUP'),
    path('home/', views.home, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=forms.LoginForm), name='login'),
]
