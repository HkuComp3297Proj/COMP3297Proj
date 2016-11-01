from django.db import models

# Create your models here.

from course.models import Course

#TODO: inside html, using a ChoiceField to indicate possible choice of sequence. The idea of validator should be discarded. If so, in the view of create_module, we should pass the number_of_module to the webpage and make it as a static field. The same with the sequence in component. Or, make the sequence as a ChoiceField with a custom __init__() function. The second method is preferred.
class Module(models.Model):
    name = models.CharField(max_length=200)
    # number_of_component = models.PositiveIntegerField(default=0, editable=False)
    number_of_component = models.PositiveIntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    sequence = models.PositiveIntegerField()


    def __str__(self):
        return self.name

    def create_component(self, name):
        pass

    def delete_component(self, sequence):
        pass

    def insert_component(self, past_seq, future_seq):
        pass

    def save(self, *args, **kwargs):
        seq = self.sequence
        self.sequence = self.course.number_of_module
        super(Module, self).save(*args, **kwargs)
        if seq < self.sequence:
            self.course.insert_module(self.sequence, seq)
        course = self.course
        course.number_of_module = course.module_set.count()
        course.save()

    def delete(self):
        for module in self.course.module_set.all():
            if module.sequence > self.sequence:
                module.sequence -= 1
        super(Module, self).delete()
