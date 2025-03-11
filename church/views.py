# church/views.py
import os  # Add this import
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Event, Sermon, ContactMessage, ImageUpload
from .forms import ContactForm, EventForm


def home(request):
    latest_events = Event.objects.order_by('-date')[:3]
    latest_sermons = Sermon.objects.order_by('-date')[:3]
    uploaded_images = ImageUpload.objects.all()
    
    # Image filtering with safe fallbacks
    hero_images = uploaded_images.filter(category='hero')[:2] if uploaded_images.filter(category='hero').exists() else [
        'img/homepage3.png', 'img/homepage.png',
    ]
    
    # Gallery images with fallback
    gallery_images = uploaded_images.filter(category='gallery')[:6]
    if not gallery_images.exists():
        gallery_images = [{'image': {'url': '/static/img/default-gallery.jpg'}}] * 6  # Fallback list
    else:
        # Check each image file exists; replace with fallback if missing
        gallery_images = [
            image if os.path.exists(os.path.join(settings.MEDIA_ROOT, image.image.name)) 
            else {'image': {'url': '/static/img/default-gallery.jpg'}}
            for image in gallery_images
        ]
    
    service_images = [
        'img/service1.jpeg',
        'img/service2.jpeg',
        'img/service3.jpg',
        'img/service4.jpeg',
    ]
    
    event_images = uploaded_images.filter(category='event')[:3] if uploaded_images.filter(category='event').exists() else []
    pastor_images = uploaded_images.filter(category='pastor')[:2] if uploaded_images.filter(category='pastor').exists() else [
        {'name': 'DR. D.K. Olukoya', 'image': 'img/gallery21.jpg', 'designation': 'GENERAL OVERSEER'},
        {'name': 'David Popoola', 'image': 'img/gallery22.jpeg', 'designation': 'REGIONAL OVERSEER'},
    ]
    
    events_with_images = [
        {'event': event, 'image': event_images[i].image.url if i < len(event_images) and event_images[i].image else None}
        for i, event in enumerate(latest_events)
    ]
    context = {
        'latest_events': events_with_images,
        'latest_sermons': latest_sermons,
        'logo': 'img/logo4.png',
        'hero_images': hero_images,
        'gallery_images': gallery_images,
        'service_images': service_images,
        'pastor_images': pastor_images,
        'favicon': 'img/favicon.jpeg',
    }
    return render(request, 'church/index.html', context)

# Rest of your views (event_list, sermon_list, contact, event_create, about) remain unchanged
def event_list(request):
    events = Event.objects.order_by('-date')
    return render(request, 'church/event_list.html', {'events': events})

def sermon_list(request):
    sermons = Sermon.objects.order_by('-date')
    return render(request, 'church/sermon_list.html', {'sermons': sermons})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            send_mail(
                form.cleaned_data['subject'],
                f"From: {form.cleaned_data['name']} ({form.cleaned_data['email']})\n\n{form.cleaned_data['message']}",
                form.cleaned_data['email'],
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
            messages.success(request, 'Your message has been sent successfully!')
            return render(request, 'church/contact.html', {'form': ContactForm()})
    else:
        form = ContactForm()
    return render(request, 'church/contact.html', {'form': form})

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'church/event_form.html', {'form': form})

def about(request):
    uploaded_images = ImageUpload.objects.all()
    
    # Filter for General Overseer and Regional Pastor
    overseer_image = uploaded_images.filter(category='pastor', description__icontains='general').first()
    overseer_image_url = overseer_image.image.url if overseer_image and overseer_image.image else 'img/gallery21.jpg'
    
    regional_image = uploaded_images.filter(category='pastor', description__icontains='regional').first()
    regional_image_url = regional_image.image.url if regional_image and regional_image.image else 'img/gallery22.jpeg'
    
    context = {
        'overseer': {
            'name': 'Dr. Daniel Kolawole Olukoya',
            'title': 'General Overseer',
            'bio': 'Dr. Daniel Kolawole Olukoya is the founder and General Overseer of Mountain of Fire and Miracles Ministries worldwide. With a Ph.D. in Molecular Genetics, he combines intellectual rigor with spiritual depth. Known for his powerful teachings on deliverance and prayer, Dr. Olukoya has authored numerous books and led the ministry to impact millions globally since its inception in 1989.',
            'image': overseer_image_url,
        },
        'regional': {
            'name': 'Pastor David Popoola',
            'title': 'Regional Pastor',
            'bio': 'Pastor David Popoola serves as the Regional Pastor of MFM Dallas. With years of dedicated service, he oversees the spiritual and administrative growth of the Dallas branch. His passion for community outreach and soul-winning has strengthened the ministry’s presence in Texas, fostering a vibrant congregation rooted in prayer and worship.',
            'image': regional_image_url,
        },
    }
    return render(request, 'church/about.html', context)

