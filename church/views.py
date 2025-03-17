# church/views.py
import os  # Add this import
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Event, Sermon, ContactMessage, ImageUpload
from .forms import ContactForm, EventForm


# church/views.py
from django.shortcuts import render
from django.conf import settings
import os
from .models import Event, Sermon, ImageUpload

def home(request):
    # Fetch latest events and sermons
    latest_events = Event.objects.order_by('-date')[:3]
    latest_sermons = Sermon.objects.order_by('-date')[:3]
    uploaded_images = ImageUpload.objects.all()

    # Hero images from admin uploads
    hero_images = uploaded_images.filter(category='hero')[:2]
    if not hero_images.exists():
        hero_images = [
            {'image': {'url': '/static/img/homepage3.png'}},
            {'image': {'url': '/static/img/homepage.png'}},
        ]

    gallery_images = uploaded_images.filter(category='gallery')[:6]
    if not gallery_images.exists():
        gallery_images = [{'image': {'url': '/static/img/default-gallery.jpg'}}] * 6
        print("No gallery uploads, using fallback")
    else:
        gallery_images = [{'image': {'url': image.image.url}} for image in gallery_images]
        print("Gallery Images Count:", len(gallery_images))
        print("Gallery Images URLs:", [img['image']['url'] for img in gallery_images])
    # Pad with fallback if less than 6
    while len(gallery_images) < 6:
        gallery_images.append({'image': {'url': '/static/img/default-gallery.jpg'}})
        print("Padded with fallback, new count:", len(gallery_images))

    # Service images from admin uploads
    service_images = uploaded_images.filter(category='service')[:4]
    if not service_images.exists():
        service_images = [
            {'image': {'url': '/static/img/service1.jpeg'}},
            {'image': {'url': '/static/img/service2.jpeg'}},
            {'image': {'url': '/static/img/service3.jpg'}},
            {'image': {'url': '/static/img/service4.jpeg'}},
        ]

    # Event images from admin uploads
    event_images = uploaded_images.filter(category='event')[:3]
    events_with_images = [
        {'event': event, 'image': event_images[i].image.url if i < len(event_images) and event_images[i].image else None}
        for i, event in enumerate(latest_events)
    ]

    # Pastor images from admin uploads
    # Pastor images (fixed)
    # Pastor images
    pastor_images = uploaded_images.filter(category='pastor')[:2]
    if not pastor_images.exists():
        pastor_images = [
            {'name': 'DR. D.K. Olukoya', 'image': {'url': '/static/img/gallery21.jpg'}, 'designation': 'GENERAL OVERSEER'},
            {'name': 'David Popoola', 'image': {'url': '/static/img/gallery22.jpeg'}, 'designation': 'REGIONAL OVERSEER'},
        ]
    else:
        designation_map = {
            'DR. D.K. Olukoya': 'GENERAL OVERSEER',
            'David Popoola': 'REGIONAL OVERSEER',
        }
        pastor_images = [
            {
                'name': image.description or 'Pastor',
                'image': {'url': image.image.url},
                'designation': designation_map.get(image.description, 'Church Leader')
            }
            for image in pastor_images
        ]
    print("Pastor Images Full Data:", [
        {'name': p['name'], 'image': p['image']['url'], 'designation': p['designation']}
        for p in pastor_images
    ])

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

