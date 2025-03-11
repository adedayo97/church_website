from django.contrib import admin
from .models import ImageUpload
from .models import ContactMessage

admin.site.register(ContactMessage)

admin.site.register(ImageUpload)
