from django.db import models
from PIL import Image

# Create your models here.
class ImageModel(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    processed = models.BooleanField(default=False)
    message = models.TextField(max_length=256, null=True, blank=True)