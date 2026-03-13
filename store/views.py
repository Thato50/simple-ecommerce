from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem

# Register
def register_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)

        return redirect('product_list')

    return render(request, 'store/register.html')


# Login
def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('product_list')

    return render(request, 'store/login.html')


# Logout
def logout_user(request):

    logout(request)

    return redirect('product_list')


# Display all products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


# Display one product's details
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})


# Display the user's cart
def cart(request):
    order, created = Order.objects.get_or_create(
        user=request.user,
        completed=False
    )

    items = order.orderitem_set.all()

    return render(request, 'store/cart.html', {
        'order': order,
        'items': items
    })


# Add product to cart
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    # get or create the cart
    order, created = Order.objects.get_or_create(
        user=request.user,
        completed=False
    )

    # get or create the cart item
    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product
    )

    # increase quantity
    order_item.quantity += 1
    order_item.save()

    return redirect('cart')

# Increase quantity
def increase_quantity(request, product_id):
    product = Product.objects.get(id=product_id)

    order = Order.objects.get(user=request.user, completed=False)

    order_item = OrderItem.objects.get(order=order, product=product)

    order_item.quantity += 1
    order_item.save()

    return redirect('cart')

#Decrease quantity
def decrease_quantity(request, product_id):
    product = Product.objects.get(id=product_id)

    order = Order.objects.get(user=request.user, completed=False)

    order_item = OrderItem.objects.get(order=order, product=product)

    order_item.quantity -= 1

    if order_item.quantity <= 0:
        order_item.delete()
    else:
        order_item.save()

    return redirect('cart')

#Remove/delet from cart
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    order = Order.objects.get(user=request.user, completed=False)

    order_item = OrderItem.objects.get(order=order, product=product)

    order_item.delete()

    return redirect('cart')