from django.shortcuts import render,redirect, get_object_or_404
from .forms import SignupForm, ContactUsForm, LoginForm, ReviewForm, UserProfileForm
from items.models import Category, Items
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Review
from core.models import UserProfile


def index(request):
    request.session.flush()
    pro=Items.objects.all().filter(for_sale=True)
    # Get all categories
    visible_categories = Category.objects.all().filter(items__in=pro).distinct()
    return render(request,'core/index.html',{'pro':pro,'cat':visible_categories})

@login_required(login_url='login')
def home(request):
      pro = Items.objects.all().filter(for_sale=True).exclude(owned_by=UserProfile.get_profile_by_user(request.user))
    # Get all categories
      visible_categories = Category.objects.all().filter(items__in=pro).distinct()
      return render(request,'items/items.html',{'pro':pro,'cat':visible_categories})

@login_required(login_url='login')
def profile(request):
    user_profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # Update User model fields

            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.username = form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            user_profile.phone = form.cleaned_data['phone'] 
            user_profile.bio = form.cleaned_data['bio']
            user_profile.address = form.cleaned_data['address']
            
            if form.cleaned_data['date_of_birth'] :
                 user_profile.date_of_birth = form.cleaned_data['date_of_birth']
                 user_profile.age = user_profile.get_age()
            
            if form.cleaned_data.get('photo'):
                user_profile.photo = form.cleaned_data['photo']

            request.user.save()
            user_profile.save()
 
            
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
def filter(request):
    query = request.GET.get('query', '')
    filters = request.GET.getlist('filters')

    # Get all categories
    cat = Category.objects.all()

    # Get all products
    pro = Items.objects.filter(for_sale=True)

    # Apply filters if a query is provided
    if query:
        if 'name' in filters:
            pro = pro.filter(name__icontains=query)
        if 'seller' in filters:
            pro = pro.filter(owned_by__user__username__icontains=query)
        if 'category' in filters:
            pro = pro.filter(category__name__icontains=query)
        else:
            pro = pro.filter(
                name__icontains=query
            ) | pro.filter(
                owned_by__user__username__icontains=query
            ) | pro.filter(
                category__name__icontains=query
            )

    # Filter out categories with no visible items
    visible_categories = cat.filter(items__in=pro).distinct()

    context = {
        'cat': visible_categories,
        'pro': pro,
        'query': query,
        'filters': filters,
    }
    return render(request, 'core/index.html', context)



