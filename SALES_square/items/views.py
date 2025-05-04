from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Items

def item(request, item_id):
    # Fetch the specific item by its ID
    product = get_object_or_404(Items, id=item_id)
    context = {
        'product': product,
        'reviews': product.reviews.all(),
    }
    return render(request, 'items/item.html', context)

def items(request):
    pro=Items.objects.all().filter(for_sale=True)
    # Get all categories
    visible_categories = Category.objects.all().filter(items__in=pro).distinct()
    return render(request,'core/index.html',{'pro':pro,'cat':visible_categories})
#will edit
def filter1(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category')  # Use 'category' instead of 'category_id'
    category = get_object_or_404(Category, id=category_id)

    # Get products
    products = Items.objects.filter(for_sale=True) & Items.objects.filter(category=category)
    products = products.filter(
        name__icontains=query
    ) | products.filter(
        Q(owned_by__user__first_name__icontains=query) | Q(owned_by__user__last_name__icontains=query)
    )

    context = {
        'category': category,
        'products': products,
        'query': query,
    }
    return render(request, 'items/category_detail.html', context)

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Items.objects.filter(category=category, for_sale=True)
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'items/category_detail.html', context)