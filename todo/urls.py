
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name="home"),
    path('task/update/<int:pk>/', views.task_update_view, name="task_update"),
    path('task/delete/<int:pk>/', views.task_delete_view, name="task_delete"),
    path('task/archive/<int:pk>/', views.task_update_to_archive_view, name="task_archive"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.logout_page, name="logout"),
]
