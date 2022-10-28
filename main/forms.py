from django.forms import ModelForm
from main.models import SourceImage

class SourceImageForm(ModelForm):

    class Meta:
        model = SourceImage
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(SourceImageForm, self).__init__(*args, **kwargs)
       
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})
        self.fields['upload_image'].required = False
        