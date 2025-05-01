from django.shortcuts import render, get_object_or_404
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
    return render(request,'items/items.html',{'pro':pro,'cat':visible_categories})
def filter1(request):
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
    return render(request, 'items/items.html', context)