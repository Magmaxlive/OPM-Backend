from django.db.models.signals import post_save,post_delete
from django.db import transaction
from django.dispatch import receiver
from .models import (Blog)
from .utils import notify_nextjs

def handle_blogs(sender,instance,signal,**kwargs):
    if signal == post_delete:
        transaction.on_commit(lambda: notify_nextjs('blogs'))
    else:
        notify_nextjs('blogs')

@receiver([post_save,post_delete],sender=Blog)
def handle_blogSection(sender,instance,signal,**kwargs):
    handle_blogs(sender,instance,signal,**kwargs)