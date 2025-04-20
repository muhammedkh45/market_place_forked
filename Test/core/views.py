from django.shortcuts import render,redirect, get_object_or_404
from .forms import SignupForm, ContactUsForm
from items.models import Category, Items
def index(request):
    return render(request, 'core/index.html',{'pro':Items.objects.all(),'cat':Category.objects.all()})

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



