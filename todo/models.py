from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=(
        ("todo", "Bajarish kerak"),
        ("complated", "Tugallangan"),
        ("archive", "Arxivda, Kelajakda bajaraman."),
    ))
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.task} | {self.user}"
    