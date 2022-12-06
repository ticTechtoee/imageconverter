from django.db import models

class SourceImage(models.Model):
    order_number = models.CharField(max_length = 50, null= False, blank = False, default = "Order Number")
    upload_image = models.ImageField(upload_to='source_images/', blank=True, null = True)

class NameNumberOrderNumber(models.Model):
    name = models.CharField(max_length = 30, null= False, blank = False, default = "Name")
    number = models.CharField(max_length = 30, null= False, blank = False, default = "Number")
    order_number = models.CharField(max_length = 50, null= False, blank = False, default = "Order Number")