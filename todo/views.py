from django.shortcuts import render, redirect
from .models import TodoList
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def home_page(request):
    if not request.user.is_authenticated:
        return redirect("login")
    data = {
        "user": request.user,
    }
    return render(request, 'index.html', context=data)


def login_page(request):
    data = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        data['error'] = "username yoki parol xato"
    return render(request, 'login.html', context=data)


def register_page(request):
    data = {}
    if request.method == "POST":
        ism = request.POST.get("first_name")
        familya = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.filter(username=username)
        if user:
            data['error'] = "bu foydalanuvchi mavjud!"
        else:
            user = User.objects.create(
                first_name=ism,
                last_name=familya,
                username=username
            )
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('home')
    return render(request, 'register.html', context=data)


def logout_page(request):
    logout(request)
    return redirect("login")