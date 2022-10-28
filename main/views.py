from django.shortcuts import render
from django.conf import settings
from .forms import SourceImageForm
from .models import SourceImage
from datetime import datetime
from django.http import FileResponse

from PIL import Image
import numpy as np


def index(request):
    form = SourceImageForm()
    if request.method == "POST":
        form = SourceImageForm(request.POST, request.FILES)
        if form.is_valid():
            ins = form.save()
            get_image = SourceImage.objects.get(id = ins.id)       
            file_name = convert_image(settings.MEDIA_ROOT +"/"+get_image.upload_image.name)
            response = FileResponse(open(file_name, 'rb'))
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
    