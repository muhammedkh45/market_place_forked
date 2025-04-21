from django.shortcuts import render,redirect, get_object_or_404
from .forms import SignupForm, ContactUsForm, LoginForm, ReviewForm, UserProfileForm
from items.models import Category, Items
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Review

def index(request):
    request.session.flush()
    return render(request, 'core/index.html',{'pro':Items.objects.all(),'cat':Category.objects.all()})

@login_required(login_url='login')
def home(request):
    return render(request,'items/items.html',{'pro':Items.objects.all(),'cat':Category.objects.all()})

@login_required(login_url='login')
def profile(request):
    user_profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # Update User model fields
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            
            # Save profile form
            profile = form.save(commit=False)
            if 'photo' in request.FILES:
                profile.photo = request.FILES['photo']
            profile.save()
            
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    context = {
        'user': request.user,
        'profile': user_profile,
        'form': form,
    }
    return render(request, 'core/profile.html', context)

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

def item(request, pk):
    item = get_object_or_404(Items, pk=pk)
    reviews = Review.objects.filter(item=item).order_by('-created_at')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to leave a review.')
            return redirect('login')
            
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been posted!')
            return redirect('item', pk=item.pk)
    else:
        form = ReviewForm()
    
    context = {
        'item': item,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'core/item.html', context)



