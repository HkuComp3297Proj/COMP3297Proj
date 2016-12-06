from django import forms
from embed_video.fields import EmbedVideoFormField

class Course_form(forms.Form):
    name = forms.CharField(label='Course name', max_length=100)
    description = forms.CharField(label='Description', widget=forms.Textarea, max_length=1000)

class Module_form(forms.Form):
    name = forms.CharField(label='Module name', max_length=100)
    sequence = forms.IntegerField(label='Sequence', min_value=1,required=False)

class Text_Component_form(forms.Form):
    name = forms.CharField(label='Component name', max_length=100)
    sequence = forms.IntegerField(label='Sequence', min_value=1,required=False)
    text_field = forms.CharField(label='Text', widget=forms.Textarea, max_length=1000)

class Image_Component_form(forms.Form):
    name = forms.CharField(label='Component name', max_length=100)
    sequence = forms.IntegerField(label='Sequence', min_value=1,required=False)
    image_field = forms.ImageField(label='Image')

class File_Component_form(forms.Form):
    name = forms.CharField(label='Component name', max_length=100)
    sequence = forms.IntegerField(label='Sequence', min_value=1,required=False)
    file_field = forms.FileField(label='File')

class Video_Component_form(forms.Form):
    name = forms.CharField(label='Component name', max_length=100)
    sequence = forms.IntegerField(label='Sequence', min_value=1,required=False)
    url_field = EmbedVideoFormField(label='Video Url')
