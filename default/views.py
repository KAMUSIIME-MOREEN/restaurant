from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import Food, Orders
import json

# Create your views here.
def home_page(request, *args, **kwargs):
    if request.method == "POST":
        if request.user.is_authenticated:
            id = request.POST['id']
            quantity = request.POST['quantity']
            location = request.POST['location']
            food_element = Food.objects.get(id=id)
            food_price = food_element.price
            total_amount = int(food_price)*int(quantity)
            Orders.objects.create(
                owner = User.objects.get(username = request.user.username),
                order = Food.objects.get(id=id),
                qty = quantity,
                price = total_amount,
                location = location
            )
            return HttpResponse(json.dumps({"message":"order placed successfully"}))
        return HttpResponse(json.dumps({"message":"please login to place order"}))
    food_id = request.GET.get("id")
    if food_id:
        food = Food.objects.get(id=food_id)
        context = {
            "food":food
        }
        return render(request, "request_order.html", context)
    food = Food.objects.all().order_by("?")
    context = {
        "food":food
    }
    response = render(request, "index.html", context)
    return response

def reg_page(request, *args, **kwargs):
    if request.method == "POST":
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        username = request.POST['uname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password ==  password2:
            try:
                user = User.objects.create(
                    first_name = firstname,
                    last_name = lastname,
                    email = email,
                    username = username
                )
                user.set_password(password)
                user.save()
                messages.info(request,"Account Created Successfully!")
            except:
                messages.info(request,"User with the same username existent in the system")
        else:
            messages.info(request,"passwords do not match")

    context = {
    }
    response = render(request, "reg.html", context)
    return response

def login_page(request, *args, **kwargs):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            print("login successfull")
            message = "login successfull"
            #messages.info(request, message)
            if request.user.is_superuser:
                return redirect("/orders/")
            else:
                return redirect("/")
        else:
            print("invalid credentials")
            message = "invalid credentials"
            messages.info(request, message)
    context = {
    }
    response = render(request, "login.html", context)
    return response

def logout_page(request, *args, **kwargs):
    logout(request)
    return redirect("/login/")


@login_required(login_url="/login/")
def orders_page(request, *args, **kwargs):
    id = request.GET.get("id")
    if id: 
        order = Orders.objects.get(id = id)
        if order.confirmed == True:
            order.confirmed = False
            order.save()
            return HttpResponse(json.dumps({"message":"confirm"}))
        else:
            order.confirmed = True
            order.save()
            return HttpResponse(json.dumps({"message":"order confirmed"}))
    orders = Orders.objects.all()
    print(orders)
    context = {
        "orders":orders
    }
    response = render(request, "orders.html", context)
    return response