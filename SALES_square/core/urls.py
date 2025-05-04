from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',views.index,name='Index'),
    path('about',views.about,name="About"),
    path('contactus',views.contactus,name='ContactUs'),
    path('terms',views.terms,name='TermsandPolicy'),
    path('signup/',views.signup_page,name='signUP'),
    path('api/signup/', views.SignupView.as_view(), name='signup'),
    path('home/', views.home, name='index'),
    path('api/login/', views.login, name='login_api'),
    path('login/', views.login_page, name='login'),
    path('', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('filter/', views.filter, name='filter'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),

]
