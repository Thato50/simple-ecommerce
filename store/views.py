from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()  # get all products from database
    return render(request, 'store/product_list.html', {'products': products})