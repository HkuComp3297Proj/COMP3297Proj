from django.contrib import admin

# Register your models here.

from .models import Category, Course, User, Module, Component_Text, Component_File, Component_Image, Enrollment

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(User)
admin.site.register(Module)
admin.site.register(Component_Text)
admin.site.register(Component_File)
admin.site.register(Component_Image)
admin.site.register(Enrollment)
