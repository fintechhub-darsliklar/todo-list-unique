from django.shortcuts import render, redirect,  get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import TodoList
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.utils import timezone
# Create your views here.


def home_page(request):
    if not request.user.is_authenticated:
        return redirect("login")
    is_created = True
    if request.method == "POST":
        date = request.POST.get("task-date")
        time = request.POST.get("task-time")
        hozir = timezone.now()
        # date va time ni birlashtiramiz
        task_datetime = datetime.strptime(
            f"{date} {time}",
            "%Y-%m-%d %H:%M"
        )
        # Agar timezone ishlatayotgan bo'lsang:
        task_datetime = timezone.make_aware(task_datetime)
        if task_datetime >= hozir:
            
            task = TodoList.objects.create(
                task=request.POST.get("task-title"),
                description=request.POST.get("task-desc"),
                status=request.POST.get("task-status"),
                date=date,
                time=request.POST.get("task-time"),
                user=request.user
            )
            is_created = True
        return redirect("home")
    status_filter = request.GET.get('status_filter', "all")
    tasks = TodoList.objects.filter(user=request.user).exclude(status='archive').order_by("date")
    if status_filter != "all":
        tasks = tasks.filter(status=status_filter)
    paginator = Paginator(tasks, 5) # Show 10 items per page
    page_number = int(request.GET.get('page', 1))
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)
    pages_range = list(range(1, len(tasks) // 5 +2))
    data = {
        "user": request.user,
        "tasks": page_obj,
        "is_created": is_created,
        "jami": len(tasks),
        "pages": pages_range,
        "current_page": page_number,
        "status_filter": status_filter,
        "all_status": {'all': {"title": "Barchasi"}, 'todo': {"title": "Bajarish kerak"}, 'complated': {"title": "Bajarilgan"}, 'archive': {"title": "Arxivdagi"}}
    }
    return render(request, 'index.html', context=data)


def task_update_view(request, pk):
    task = get_object_or_404(TodoList, id=pk, user=request.user)

    if request.method == "POST":
        task.task = request.POST.get("task-title")
        task.description = request.POST.get("task-desc")
        task.status = request.POST.get("task-status")
        # task.date = request.POST.get("task-date")
        task.time = request.POST.get("task-time")
        task.save()

    return redirect("home")


def task_delete_view(request, pk):
    task = get_object_or_404(TodoList, id=pk, user=request.user)
    if task:
        task.delete()
    return redirect("home")
    
       
def task_update_to_archive_view(request, pk):
    task = get_object_or_404(TodoList, id=pk, user=request.user)
    if task:
        task.status = 'archive'
        task.save()
    return redirect("home") 


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