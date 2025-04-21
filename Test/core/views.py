from django.shortcuts import render,redirect, get_object_or_404
from .forms import SignupForm, ContactUsForm, LoginForm
from items.models import Category, Items
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def index(request):
    request.session.flush()
    return render(request, 'core/index.html',{'pro':Items.objects.all(),'cat':Category.objects.all()})

@login_required(login_url='login')
def home(request):
    return render(request,'items/items.html',{'pro':Items.objects.all(),'cat':Category.objects.all()})


def about(request):
    return render(request,'core/about.html', {})


def contactUS(request):
    return render(request,'core/contactus.html', {})

def terms(request):
    return render(request,'core/terms.html', {})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })


def contactus(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ContactUsForm()

    return render(request, 'core/contactus.html', {
        'form': form
    })


class CustomLoginView(auth_views.LoginView):
    template_name = 'core/login.html'
    authentication_form = LoginForm

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)



