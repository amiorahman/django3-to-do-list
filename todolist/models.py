from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True)