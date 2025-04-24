from django.shortcuts import render, get_object_or_404
from .models import Category, Items

def item(request, item_id):
    # Fetch the specific item by its ID
    product = get_object_or_404(Items, id=item_id)
    context = {
        'product': product,
    }
    return render(request, 'items/item.html', context)

def items(request):
    return render(request,'items/items.html',{'pro':Items.objects.all(),'cat':Category.objects.all()})
