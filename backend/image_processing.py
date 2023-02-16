import os
import random

from PIL import Image, ImageEnhance, ImageFilter
from PIC.settings import BASE_DIR, STATICFILES_DIRS
from .models import ImageModel

def overlay(image, overlay_img):
    x, y = image.size
    overlays_path = os.path.join(STATICFILES_DIRS[0], 'processing')
    overlay = Image.open(os.path.join(overlays_path, overlay_img)).convert('RGBA')
    if x > y:
        overlay = overlay.transpose(Image.ROTATE_90)
    overlay = overlay.resize((x, y))
    image.paste(overlay, (0,0), overlay)
    return image

def cattack(image):
    x_image, y_image = image.size
    overlays_path = os.path.join(STATICFILES_DIRS[0], 'processing')
    overlay = Image.open(os.path.join(overlays_path, 'Cattack.png')).convert('RGBA')
    image = image.filter(ImageFilter.GaussianBlur(radius=5))
    converter = ImageEnhance.Color(image)
    image = converter.enhance(0.3)
    x_overlay, y_overlay = overlay.size
    image.paste(overlay, (int(x_image/2) - int(x_overlay/2), y_image - y_overlay), overlay)
    message = "Cattack!!!!"
    return image, message

def ketchup_splash(image):
    overlay_img = 'blood-splatter.png'
    image = overlay(image, overlay_img)
    message = "Uhmm... Don't worry, it's just ketchup... yeah."
    return image, message

def cat_slash(image):
    overlay_img = 'cat_slash.png'
    image = overlay(image, overlay_img)
    message = "Oops! Randy's cat got angry. At least... we hope it was the cat."
    return image, message

def cat_prints(image):
    overlay_img = 'Paw-Print.png'
    image = overlay(image, overlay_img)
    message = "Oops! Randy brought his cat to work again."
    return image, message

def smoke(image):
    overlay_img = "Smoke.png"
    image = overlay(image, overlay_img)
    message = "Someone is smoking! Hopefully, it's Randy and not the server."
    return image, message

def blurred(image):
    image = image.filter(ImageFilter.GaussianBlur(radius=10))
    message = "Image looks fine for us. We think you might need glasses."
    return image, message

def weird_colors_mirror(image):
    r, g, b = image.split()
    image = Image.merge('RGB', (b, g, r))
    image = image.transpose(Image.FLIP_LEFT_RIGHT)
    message = "Oops! We suspect Randy might've been drinking on the job"
    return image, message

def process_image(id):
    image_path = (ImageModel.objects.get(id=id)).image.path
    image_path = os.path.join(BASE_DIR, image_path)
    image = Image.open(image_path)
    size = (1024,1024)
    image.thumbnail(size)
    random_choice = random.randrange(8)

    match random_choice:
        case 0:
            image, message = cattack(image)
        case 1:
            image, message = ketchup_splash(image)
        case 2:
            image, message = cat_slash(image)
        case 3:
            image, message = cat_prints(image)
        case 4:
            image, message = smoke(image)
        case 5:
            image, message = blurred(image)
        case 6:
            image, message = weird_colors_mirror(image)
    image.save(image_path)
    return message
