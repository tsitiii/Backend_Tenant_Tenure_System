from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from .models import Notification

@receiver(post_save, sender=Notification)
def post_save_notification(sender, instance, created, **kwargs):
    pass