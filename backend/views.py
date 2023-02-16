from django.shortcuts import render, redirect
from .models import ImageModel
from .forms import ImageForm
from .image_processing import *
import os
# Create your views here.

def image_upload_view(request):
    form = ImageForm(request.POST or None)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.save()
            id = image.id
            return redirect(f'/{id}')
    else:
        context = {
            'form' : form
        }
        return render(request, 'images/image_upload.html', context)

def image_view(request, id):
    image = ImageModel.objects.get(id=id)
    print(image.processed)
    if image.processed == False:
        image.processed = True
        image.message = process_image(id)
        image.save()
    context = {
        'image': image
    }
    print(image.processed)
    return render(request, 'images/image_show.html', context)