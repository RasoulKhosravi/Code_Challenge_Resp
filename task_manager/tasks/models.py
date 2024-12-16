from django.db import models
from django.conf import settings

class Task(models.Model):
    STATUS_CHOICES = (('In Progress', 'In Progress'),('Completed', 'Completed'),)
    title = models.CharField(max_length=255)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')

    def is_owner(self, user):
        return self.user == user
        
    def __str__(self):
        return self.title
