from django.contrib import admin

# Register your models here.

from .models import Component_Text, Component_File, Component_Image

admin.site.register(Component_Text)
admin.site.register(Component_File)
admin.site.register(Component_Image)
