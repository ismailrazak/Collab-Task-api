from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings

@receiver(pre_save,sender=settings.AUTH_USER_MODEL)
def username_generation(sender,instance,**kwargs):
    print(instance.username)
    if not instance.username:
        username = f'{instance.first_name}_{instance.last_name}'
        counter=0
        while(get_user_model().objects.filter(username=username).exists()):
            username = f'{instance.first_name}_{instance.last_name}_{counter}'
            counter+=1
        instance.username = username
    #NO NEED TO SAVE FOR PRE SAVE CAUSE IT SAVES ALREADY
