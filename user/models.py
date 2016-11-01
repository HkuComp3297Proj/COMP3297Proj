from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=8, unique=True)
    password = models.CharField(max_length=200)
    identity_instructor = models.BooleanField(default=False)
    identity_admin = models.BooleanField(default=False)
    identity_hr = models.BooleanField(default=False)
    current_enrollment = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def change_Identity(self, identity, set_value):
        pass

class Particiapnt(User):
    class Meta:
        proxy = True

    def enroll(self, course_ID):
        pass

    def drop(self, course_ID):
        pass

class Instructor(User):
    class Meta:
        proxy = True

class Administrator(User):
    class Meta:
        proxy = True

    def create_category(self, name):
        pass

class HR(User):
    class Meta:
        proxy = True
