from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from course.models import Course
from category.models import Category

@receiver(post_save, sender=Course)
@receiver(post_delete, sender=Course)
def model_post_change(sender, **kwargs):
    categories = Category.objects.all()
    for category in categories:
        category.number_of_course = category.course_set.count()
        category.save()
