from django.db.models.signals import post_init, post_save
from django.dispatch import receiver
from django.template.base import kwarg_re
from django.utils import timezone

from house.models import House

from .models import COMPLETED, NOT_COMPLETED, Task, TaskList


@receiver(post_save, sender=Task)
def update_house_points(sender, instance, created, **kwargs):
    if not created:
        house = instance.tasklist.house
        if instance.status == COMPLETED:
            house = instance.tasklist.house
            house.points += 10
            house.save()
        elif instance.status == NOT_COMPLETED:
            if not house.points <= 0:
                house.points -= 10
                house.save()


@receiver(post_init, sender=Task)
def remember_task_status(instance, **kwargs):
    instance.previous_status = instance.status


@receiver(post_save, sender=Task)
def update_tasks_count(instance, created, **kwargs):
    if not created:
        house = instance.tasklist.house
        tasklist = instance.tasklist
        if instance.previous_status != instance.status:
            completed_tasks_count = tasklist.tasks.filter(status=COMPLETED).count()
            house.completed_tasks_count = completed_tasks_count
            not_completed_tasks_count = tasklist.tasks.filter(
                status=NOT_COMPLETED
            ).count()
            house.not_completed_tasks_count = not_completed_tasks_count
            house.save()


@receiver(post_save, sender=Task)
def update_tasklist_status(instance, created, **kwargs):
    if not created:
        house = instance.tasklist.house
        tasklist = instance.tasklist
        if not tasklist.tasks.filter(status=NOT_COMPLETED):
            tasklist.status = COMPLETED
            tasklist.completed_on = timezone.now()
            tasklist.save()
        else:
            tasklist.status = NOT_COMPLETED
            tasklist.completed_on = None
            tasklist.save()
