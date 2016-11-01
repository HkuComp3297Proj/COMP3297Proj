from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

from module.models import Module

class Component(models.Model):
    name = models.CharField(max_length=200)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    sequence = models.PositiveIntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        seq = self.sequence
        self.sequence = self.module.number_of_component
        super(Component, self).save(*args, **kwargs)
        if seq < self.sequence:
            self.module.insert_component(self.sequence, seq)
        module = self.module
        module.number_of_component = module.component_file_set.count() + module.component_text_set.count() + module.component_image_set.count()
        module.save()

    def delete(self):
        for component in self.module.component_set.all():
            if component.sequence > self.sequence:
                component.sequence -= 1
        super(Component, self).delete()

class Component_Text(Component):
    text_field = models.TextField()

class Component_Image(Component):
    image_field = models.ImageField()

class Component_File(Component):
    file_field = models.FileField()
