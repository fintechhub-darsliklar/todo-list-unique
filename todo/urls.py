
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name="home"),
    path('task/update/<int:pk>/', views.task_update_view, name="task_update"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.logout_page, name="logout"),
]
