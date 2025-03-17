# church/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
    
class Sermon(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    preacher = models.CharField(max_length=100)
    date = models.DateTimeField()
    audio_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

def upload_to_path(instance, filename):
    return f'uploads/{instance.category}/{filename}'

# church/models.py
class ImageUpload(models.Model):
    CATEGORY_CHOICES = [
        ('service', 'Service'),
        ('gallery', 'Gallery'),
        ('pastor', 'Pastor'),
        ('event', 'Event'),
        ('hero', 'Hero'),
    ]
    image = models.ImageField(upload_to=upload_to_path)
    description = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='gallery')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    designation = models.CharField(max_length=100, blank=True, null=True)  # New field

    def __str__(self):
        return f"{self.category} - {self.description or 'No description'}"