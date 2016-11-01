from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    # number_of_course = models.PositiveIntegerField(default=0, editable=False)
    number_of_course = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def create_course(self, name, category, instructor, description):
        pass
