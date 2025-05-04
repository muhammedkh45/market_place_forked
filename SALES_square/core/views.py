from django.shortcuts import render,redirect, get_object_or_404
from .forms import SignupForm, ContactUsForm, LoginForm, ReviewForm, UserProfileForm
from items.models import Category, Items
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Review
from core.models import UserProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountSignupSerializer,UserSerializer
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login as django_login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        django_login(request._request, user)  # Use request._request for Django login
        serializer = UserSerializer(user)
        return Response({"message": "Login successful", "user": serializer.data}, status=200)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
def login_page(request):
    return render(request, 'core/login.html')

"""
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
"""
class SignupView(APIView):
    def post(self, request):
        serializer = AccountSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Account created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
def signup_page(request):
    return render(request, 'core/signup.html')

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
      return render(request,'core/index.html',{'pro':pro,'cat':visible_categories})

@login_required(login_url='login')
def profile(request):
    user_profile = request.user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # Check if old password is correct
            old_password = form.cleaned_data.get('old_password')
            if old_password and not request.user.check_password(old_password):
                messages.error(request, 'The old password is incorrect.')
                return redirect('profile')

            # Check if new password matches the confirmed password
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')
            if new_password and new_password != confirm_password:
                messages.error(request, 'The new password and confirmation do not match.')
                return redirect('profile')

            # Update User model fields
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.username = form.cleaned_data['username']
            request.user.email = form.cleaned_data['email']

            # Handle phone field
            phone = form.cleaned_data['phone']
            user_profile.phone = phone if phone else None  # Set to None if empty

            user_profile.bio = form.cleaned_data['bio']
            user_profile.address = form.cleaned_data['address']

            if form.cleaned_data['date_of_birth']:
                user_profile.date_of_birth = form.cleaned_data['date_of_birth']
                user_profile.age = user_profile.get_age()

            if form.cleaned_data.get('photo'):
                user_profile.photo = form.cleaned_data['photo']

            # Update password if provided
            if new_password and  request.user.check_password(old_password):
                request.user.set_password(new_password)

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
"""
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
"""
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
"""
class CustomLoginView(auth_views.LoginView):
    template_name = 'core/login.html'
    authentication_form = LoginForm

    def form_invalid(self, form):
        # Custom error message for invalid credentials
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)
    
    def form_valid(self, form):
        # If form is valid, redirect to the appropriate page
        messages.success(self.request, 'Welcome back!')
        return super().form_valid(form)
"""
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
    return render(request, 'core/index.html', context)
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
          pro = pro.filter(
          Q(owned_by__user__first_name__icontains=query) |
          Q(owned_by__user__last_name__icontains=query)
          )        
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
# views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Avg,Count  # Add this import
from .models import UserProfile

def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        profile = user.profile
        # Only include products with rating > 0 in the calculation
        rated_products = profile.items.filter(average_rating__gt=0)
        
        rating_info = rated_products.aggregate(
            avg_rating=Avg('average_rating'),
            rated_count=Count('id')
        )
        
        avg_rating = rating_info['avg_rating'] or 0
        rated_count = rating_info['rated_count']
        total_products = profile.items.count()
        
    except UserProfile.DoesNotExist:
        avg_rating = 0
        rated_count = 0
        total_products = 0
    
    context = {
        'user_profile': profile,
        'products': profile.items.all() if hasattr(user, 'profile') else [],
        'avg_rating': avg_rating,
        'rated_count': rated_count,
        'total_products': total_products,
    }
    return render(request, 'core/user_detail.html', context)



