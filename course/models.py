from django.db import models

# Create your models here.

from category.models import Category
from user.models import Instructor

def validate_not_blank(description):
    if description == []:
        description = "This course has no description."

#TODO: add a unique validator for course name instead of set the name as unique in case there are courses in different category which have the same name. Same for module, component. To make it a static validator, it will be better in the webpage as a javascript function. Or, make it a validator with category as a parameter passed in. Or, before save, raise a validator error if the name is not unique in this category. The third solution is the simplest.
class Course(models.Model):
    name = models.CharField(max_length=200)
    # number_of_module = models.PositiveIntegerField(default=0, editable=False)
    number_of_module = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    opened = models.BooleanField(default=False)
    description = models.TextField(default="This course has no description.", validators=[validate_not_blank])


    def __str__(self):
        return self.name

    def create_module(self, name):
        pass

    def delete_module(self, sequence):
        pass

    #TODO: Are these modify, insert and delete functions should be in the class model? I prefer modify_module to be a function in the class module as it is a function that modify module itself. Insert, delete are same dunctions that only relate with Module.
    def modify_module(self, sequence, new_name):
        pass

    def insert_module(self, past_seq, future_seq):
        pass

    def open(self):
        self.opened = True;
