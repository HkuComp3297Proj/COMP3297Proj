from django.db import models
from itertools import chain
from django.contrib.auth.models import AbstractUser
from embed_video.fields import EmbedVideoField
import datetime
# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=8, unique=True)
    password = models.CharField(max_length=200)
    identity_instructor = models.BooleanField(default=False)
    identity_admin = models.BooleanField(default=False)
    identity_hr = models.BooleanField(default=False)
    current_enrollment = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    '''
    Created by Charlie Chen
    This is the interface for change the user's identity
    set_value: a list of identity of change requested by some administrator.
    '''
    def change_identity(self, set_value):
        if "Instructor" in set_value:
            self.identity_instructor = True
        else:
            self.identity_instructor = False
        if "Administrator" in set_value:
            self.identity_admin = True
        else:
            self.identity_admin = False
        if "HR" in set_value:
            self.identity_hr = True
        else:
            self.identity_hr = False
        self.save()


    def get_identity_list(self):
        identity_list = ["Participant"]
        if self.identity_instructor:
            identity_list.append("Instructor")
        if self.identity_admin:
            identity_list.append("Administrator")
        if self.identity_hr:
            identity_list.append("HR")
        return identity_list

    def change_instructor(self):
        self.identity_instructor = not self.identity_instructor
        self.save()

class Participant(User):
    class Meta:
        proxy = True

    def is_enrolled(self):
        return self.current_enrollment

    def enroll(self, course):
        if self.is_enrolled():
            return
        this_course = Course.objects.filter(name=course)[0]
        enrollment = Enrollment(participant=self, course=this_course, module_progress=0)
        self.current_enrollment = True
        enrollment.save()
        self.save()

    def drop(self, course):
        this_course = Course.objects.filter(name=course)[0]
        enrollment = self.enrollment_set.filter(course=this_course)[0]
        enrollment.delete()
        self.current_enrollment = False
        self.save()

    def update_enrollment(self):
        if not self.is_enrolled():
            return
        enrollment = self.enrollment_set.filter(completion_date__isnull=True)[0]
        enrollment.module_progress = enrollment.module_progress + 1
        if enrollment.module_progress == enrollment.course.number_of_module:
            enrollment.completion_date = datetime.date.today()
            self.current_enrollment = False
            self.save()
        enrollment.save()

class Instructor(User):
    class Meta:
        proxy = True

    @classmethod
    def get_Instructor(cls):
        return Instructor.objects.filter(identity_instructor=True)

    '''
    created by Charlie Chen
    '''
    def get_courses_instructed(self):
        pass

class Administrator(User):
    class Meta:
        proxy = True

    @classmethod
    def get_Administrator(cls):
        return Administrator.objects.filter(identity_administrator=True)

    '''
    Modified by Charlie Chen
    '''
    @classmethod
    def create_category(self, name):
        category = Category(name=name)
        category.save()

class HR(User):
    class Meta:
        proxy = True

    @classmethod
    def get_HR(cls):
        return HR.objects.filter(identity_hr=True)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    number_of_course = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    @classmethod
    def create_course(cls, name, category, instructor, description):
        course = Course(name=name, category=Category.objects.filter(name=category)[0], number_of_module=0, instructor=Instructor.get_Instructor().filter(username=instructor)[0], opened=False, description=description)
        course.save()


class Course(models.Model):
    name = models.CharField(max_length=100)
    # number_of_module = models.PositiveIntegerField(default=0, editable=False)
    number_of_module = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    opened = models.BooleanField(default=False)
    description = models.TextField(default="This course has no description.")

    # @classmethod
    # def create(cls, name, category, instructor, description):
    #     course = cls(name=name, category=category, number_of_module=0, instructor=instructor, opened=False, description=description)
    #     return course

    def __str__(self):
        return self.name

    @classmethod
    def create_module(cls, name, course, sequence):
        this_course = Course.objects.filter(name=course)[0]
        module = Module(name=name, number_of_component=0, course=this_course, sequence=this_course.number_of_module)
        module.save()
        if sequence - 1 < this_course.number_of_module:
            module.insert_module(sequence)

    def open(self):
        self.opened = True
        self.save()


class Module(models.Model):
    name = models.CharField(max_length=100)
    number_of_component = models.PositiveIntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    sequence = models.PositiveIntegerField()

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return self.name

    @classmethod
    def create_text_component(self, name, module, sequence, text_field):
        this_module = Module.objects.filter(name=module)[0]
        component = Component_Text(name=name, module=this_module, sequence=this_module.number_of_component, text_field=text_field)
        component.save()
        if sequence - 1 < this_module.number_of_component:
            component.insert_component(sequence)

    @classmethod
    def create_image_component(self, name, module, sequence, image_field):
        this_module = Module.objects.filter(name=module)[0]
        component = Component_Image(name=name, module=this_module, sequence=this_module.number_of_component, image_field=image_field)
        component.save()
        if sequence - 1 < this_module.number_of_component:
            component.insert_component(sequence)

    @classmethod
    def create_file_component(self, name, module, sequence, file_field):
        this_module = Module.objects.filter(name=module)[0]
        component = Component_File(name=name, module=this_module, sequence=this_module.number_of_component, file_field=file_field)
        component.save()
        if sequence - 1 < this_module.number_of_component:
            component.insert_component(sequence)

    @classmethod
    def create_video_component(self, name, module, sequence, url_field):
        this_module = Module.objects.filter(name=module)[0]
        component = Component_Video(name=name, module=this_module, sequence=this_module.number_of_component, url_field=url_field)
        component.save()
        if sequence - 1 < this_module.number_of_component:
            component.insert_component(sequence)

    def modify_module(self, new_name, sequence):
        self.name = new_name
        self.save()
        self.insert_module(sequence)

    def insert_module(self, future_seq):
        if future_seq - 1 == self.sequence:
            self.save()
            return
        past_seq = self.sequence
        if future_seq > self.course.number_of_module:
            self.sequence = self.course.number_of_module - 1
        else:
            self.sequence = future_seq - 1
        for s in self.course.module_set.all():
            if s!=self and s.sequence>=min(past_seq, self.sequence) and s.sequence<=max(past_seq, self.sequence):
                if past_seq<self.sequence:
                    s.sequence-=1
                elif past_seq>self.sequence:
                    s.sequence+=1
                s.save()
        self.save()

    def save(self, *args, **kwargs):
        super(Module, self).save(*args, **kwargs)
        course = self.course
        course.number_of_module = course.module_set.count()
        course.save()

    def delete(self):
        for module in self.course.module_set.all():
            if module.sequence > self.sequence:
                module.sequence -= 1
                module.save()
        super(Module, self).delete()


class Component(models.Model):
    TEXT = 'T'
    FILE = 'F'
    IMAGE = 'I'
    VIDEO = 'V'
    COMPONENT_TYPE_CHOICES = (
        (TEXT, 'Text'),
        (FILE, 'File'),
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
    )

    name = models.CharField(max_length=100)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    sequence = models.PositiveIntegerField()
    component_type = models.CharField(
        max_length=1,
        choices=COMPONENT_TYPE_CHOICES,
        default=TEXT,
    )
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Component, self).save(*args, **kwargs)
        module = self.module
        module.number_of_component = module.component_file_set.count() + module.component_text_set.count() + module.component_image_set.count() + module.component_video_set.count()
        module.save()

    def delete(self):
        all_component_list = list(chain(self.module.component_text_set.all(), self.module.component_image_set.all(), self.module.component_file_set.all(), self.module.component_video_set.all()))
        for component in all_component_list:
            if component.sequence > self.sequence:
                component.sequence -= 1
                component.save()
        super(Component, self).delete()

    def modify_component(self, new_name, sequence):
        self.name = new_name
        self.save()
        self.insert_component(sequence)

    def insert_component(self, future_seq):
        if future_seq - 1 ==self.sequence:
            self.save()
            return
        past_seq = self.sequence
        if future_seq > self.module.number_of_component:
            self.sequence = self.module.number_of_component - 1
        else:
            self.sequence = future_seq - 1
        all_component_list = list(chain(self.module.component_text_set.all(), self.module.component_image_set.all(), self.module.component_file_set.all(), self.module.component_video_set.all()))
        for s in all_component_list:
            if s!=self and s.sequence >= min(past_seq, self.sequence) and s.sequence<=max(past_seq, self.sequence):
                if past_seq < self.sequence:
                    s.sequence-=1
                elif past_seq > self.sequence:
                    s.sequence+=1
                s.save()
        self.save()
        pass

class Component_Text(Component):
    text_field = models.TextField()

    def modify_component(self, new_name, sequence, text_field):
        super(Component_Text, self).modify_component(new_name, sequence)
        self.text_field = text_field
        self.save()

    def save(self, *args, **kwargs):
        self.component_type = self.TEXT
        super(Component_Text, self).save(*args, **kwargs)

class Component_Image(Component):
    image_field = models.ImageField()

    def modify_component(self, new_name, sequence, image_field):
        super(Component_Image, self).modify_component(new_name, sequence)
        self.image_field = image_field
        self.save()

    def save(self, *args, **kwargs):
        self.component_type = self.IMAGE
        super(Component_Image, self).save(*args, **kwargs)

class Component_File(Component):
    file_field = models.FileField()

    def modify_component(self, new_name, sequence, file_field):
        super(Component_File, self).modify_component(new_name, sequence)
        self.file_field = file_field
        self.save()

    def save(self, *args, **kwargs):
        self.component_type = self.FILE
        super(Component_File, self).save(*args, **kwargs)

class Component_Video(Component):
    url_field = EmbedVideoField()

    def modify_component(self, new_name, sequence, url_field):
        super(Component_Video, self).modify_component(new_name, sequence)
        self.url_field = url_field
        self.save()

    def save(self, *args, **kwargs):
        self.component_type = self.VIDEO
        super(Component_Video, self).save(*args, **kwargs)

class Enrollment(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completion_date = models.DateField(null=True)
    module_progress = models.IntegerField(default=0)
    # component_progress = models.IntegerField(default=0)
