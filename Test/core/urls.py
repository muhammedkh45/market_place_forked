from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',views.index,name='Index'),
    path('about',views.about,name="About"),
    path('contactus',views.contactus,name='ContactUs'),
    path('terms',views.terms,name='TermsandPolicy'),
    path('signup/',views.signup,name='signUP'),
    path('home/', views.home, name='index'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('filter/', views.filter, name='filter'),
]
