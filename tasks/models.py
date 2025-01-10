import uuid
import os
from django.db import models
from django.conf import  settings
from django.utils.deconstruct import deconstructible

@deconstructible
class GenerateAttachmentFilePath:
    def __init__(self):
        pass

    def __call__(self,instance,filename):
        ext = filename.split('.')[-1]
        path = f'media/tasks/{instance.id}/attachments'
        name =f'main.{ext}'
        return os.path.join(path,name)

attachment_path = GenerateAttachmentFilePath()


NOT_COMPLETED = 'NC'
COMPLETED = 'C'

task_choices =[
    (NOT_COMPLETED,'Not Completed'),
    (COMPLETED,'Completed'),
]

class TaskList(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(blank=True, null=True)
    house = models.ForeignKey('house.House',on_delete=models.CASCADE,related_name='task_lists')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='created_task_lists',
                                   null=True, blank=True)
    status = models.CharField(max_length=2, choices=task_choices, default=NOT_COMPLETED)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Task(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(blank=True,null=True)
    completed_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name='completed_tasks',null=True,blank=True)
    created_by =  models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name='created_tasks',null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=2,choices=task_choices,default=NOT_COMPLETED)
    name = models.CharField(max_length=128)
    tasklist = models.ForeignKey('tasks.TaskList',on_delete=models.CASCADE,related_name='tasks')

    def __str__(self):
        return self.name

class Attachment(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,unique=True,default=uuid.uuid4)
    created_on = models.DateTimeField(auto_now_add=True)
    data = models.FileField(upload_to=attachment_path)
    task = models.ForeignKey('tasks.Task',on_delete=models.CASCADE,related_name='attachments')
    def __str__(self):
        return f'{self.id}_{self.task}'
