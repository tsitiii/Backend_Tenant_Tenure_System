from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from .models import Notification, BaseUser,Report

@receiver(post_save, sender=Notification)
def post_save_notification(sender, instance, created, **kwargs):
    pass


@receiver(post_save, sender=BaseUser)
def post_save_report(sender, instance, created, **kwargs):
    if created:
        report, _ = Report.objects.get_or_create(id=1)
        report.total_tenants = BaseUser.objects.filter(role='is_tenant').count()
        report.total_landlords = BaseUser.objects.filter(role='is_landlord').count()
        report.total_users = BaseUser.objects.exclude(role__in=['is_admin', 'is_witness']).count()
        report.total_admins = BaseUser.objects.filter(role='is_admin').count()
        report.total_witnesses = BaseUser.objects.filter(role='is_witness').count()
        report.save()