from django.contrib import admin
from embed_video.admin import AdminVideoMixin

# Register your models here.

from .models import Category, Course, User, Module, Component_Text, Component_File, Component_Image, Component_Video, Enrollment

class Component_Video_Admin(AdminVideoMixin, admin.ModelAdmin):
    pass

admin.site.register(Component_Video, Component_Video_Admin)

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(User)
admin.site.register(Module)
admin.site.register(Component_Text)
admin.site.register(Component_File)
admin.site.register(Component_Image)
admin.site.register(Enrollment)
