from django.shortcuts import render
from django.conf import settings
from .forms import SourceImageForm, NameNumberOrderNumberForm
from .models import SourceImage
from datetime import datetime
from django.http import FileResponse

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import numpy as np


def index(request):
    form = SourceImageForm()
    if request.method == "POST":
        form = SourceImageForm(request.POST, request.FILES)
        if form.is_valid():
            ins = form.save()
            get_image = SourceImage.objects.get(id = ins.id)       
            file_name = convert_image(settings.MEDIA_ROOT +"/"+get_image.upload_image.name)
            final_file_name = write_order_name(file_name, request.POST.get('order_number'))
            response = FileResponse(open(final_file_name, 'rb'))
            return response       
    return render(request, "main/index.html", {'form':form})

# Custom Function
def convert_image(input_image_name):
    # Reading the image using imread() function

    file_name = ""
    
    im = im = Image.open(input_image_name)
    im = im.convert('RGBA')

    data = np.array(im)   # "data" is a height x width x 4 numpy array
    
    data[..., :-1]= (255, 0, 0) # Transpose back needed
    im2 = Image.fromarray(data)
    file_name = settings.MEDIA_ROOT+"/converted_images/converted"+datetime.now().strftime('%H-%M-%S')+".tiff"
    im2.save(file_name)
    return file_name

def write_order_name(input_image_name, order_number):
    file = settings.MEDIA_ROOT+"/text_image/converted"+datetime.now().strftime('%H-%M-%S')+".tiff"
    img = Image.open(str(input_image_name))
    h = img.height - 50
    w = 20
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("Roboto-Black.ttf", 36)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((w, h),str(order_number),(0,0,0),font=font)
    img.save(file)

    return file
    


def secondPage(request):
    form = NameNumberOrderNumberForm()
    if request.method == "POST":
        form = NameNumberOrderNumberForm(request.POST,request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            number = form.cleaned_data.get('number')
            orderNumber = form.cleaned_data.get('order_number')
            finalFileName = drawImage(name, number, orderNumber)
            response = FileResponse(open(finalFileName, 'rb'))
            return response    
    return render(request, "main/second_page.html", {'form':form})

def drawImage(name, number, OrderNumber):
    file = settings.MEDIA_ROOT+"/text_image/created"+datetime.now().strftime('%H-%M-%S')+".png"
    img = Image.new('RGBA', (1008, 1008), color = (255,0, 0, 0))
    text_color = (0, 0, 0)
    outline_color = (255, 255, 255)
    h = img.height - 50
    draw = ImageDraw.Draw(img)
    txt = name
    fontsize = 1  # starting font size

    # portion of image width you want text width to be
    img_fraction = 0.50

    font = ImageFont.truetype("Roboto-Black.ttf", fontsize)
    while font.getsize(txt)[0] < img_fraction*img.size[0]:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype("Roboto-Black.ttf", fontsize)

    # optionally de-increment to be sure it is less than criteria
    fontsize -= 1
    font = ImageFont.truetype("Roboto-Black.ttf", fontsize)

    x = 0
    y = 0
    y2 = 200
    y3 = h
    bd_w = 1

    #draw.text((0, 0), txt, font=font, fill=outline_color) # put the text on the image

    #draw.text((0,200), number, font=font, fill=outline_color)
    #draw.text((0,400), OrderNumber, font=font, fill=outline_color)
    
    draw.text((x-bd_w, y), txt, font=font, fill=outline_color)
    draw.text((x, y-bd_w), txt, font=font, fill=outline_color)
    draw.text((x+bd_w, y), txt, font=font, fill=outline_color)
    draw.text((x, y+bd_w), txt, font=font, fill=outline_color)

    draw.text((x+bd_w, y-bd_w), txt, font=font, fill=outline_color)
    draw.text((x-bd_w, y-bd_w), txt, font=font, fill=outline_color)
    draw.text((x-bd_w, y+bd_w), txt, font=font, fill=outline_color)
    draw.text((x+bd_w, y+bd_w), txt, font=font, fill=outline_color)

    draw.text((x, y), txt, font=font, fill=text_color)
#----------------------------------------------------------------------------------
    draw.text((x-bd_w, y2), number, font=ImageFont.truetype("Roboto-Black.ttf", 144), fill=outline_color)
    draw.text((x, y2-bd_w), number, font=ImageFont.truetype("Roboto-Black.ttf", 144), fill=outline_color)
    draw.text((x+bd_w, y2), number, font=ImageFont.truetype("Roboto-Black.ttf", 144), fill=outline_color)
    draw.text((x, y2+bd_w), number, font=ImageFont.truetype("Roboto-Black.ttf", 144), fill=outline_color)

    draw.text((x+bd_w, y2-bd_w), number, font=ImageFont.truetype("Roboto-Black.ttf", 144), fill=outline_color)
    draw.text((x-bd_w, y2-bd_w), number, font=ImageFont.truetype("Roboto-Black.ttf", 144), fill=outline_color)
    draw.text((x-bd_w, y2+bd_w), number, font=ImageFont.truetype("Roboto-Black.ttf", 144), fill=outline_color)
    draw.text((x+bd_w, y2+bd_w), number, font=ImageFont.truetype("Roboto-Black.ttf", 144), fill=outline_color)

    draw.text((x, y2), number, font=ImageFont.truetype("Roboto-Black.ttf", 144), fill=text_color)

#----------------------------------------------------------------------------------
    draw.text((x-bd_w, y3), OrderNumber, font=ImageFont.truetype("Roboto-Black.ttf", 36), fill=outline_color)
    draw.text((x, y3-bd_w), OrderNumber, font=ImageFont.truetype("Roboto-Black.ttf", 36), fill=outline_color)
    draw.text((x+bd_w, y3), OrderNumber, font=ImageFont.truetype("Roboto-Black.ttf", 36), fill=outline_color)
    draw.text((x, y3+bd_w), OrderNumber, font=ImageFont.truetype("Roboto-Black.ttf", 36), fill=outline_color)

    draw.text((x+bd_w, y3-bd_w), OrderNumber, font=ImageFont.truetype("Roboto-Black.ttf", 36), fill=outline_color)
    draw.text((x-bd_w, y3-bd_w), OrderNumber, font=ImageFont.truetype("Roboto-Black.ttf", 36), fill=outline_color)
    draw.text((x-bd_w, y3+bd_w), OrderNumber, font=ImageFont.truetype("Roboto-Black.ttf", 36), fill=outline_color)
    draw.text((x+bd_w, y3+bd_w), OrderNumber, font=ImageFont.truetype("Roboto-Black.ttf", 36), fill=outline_color)

    draw.text((x, y3), OrderNumber, font=ImageFont.truetype("Roboto-Black.ttf", 36), fill=text_color)


    img.save(file, 'PNG') # save it
    return file