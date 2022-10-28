from django.db import models

class SourceImage(models.Model):
    upload_image = models.ImageField(upload_to='source_images/', blank=True, null = True)
