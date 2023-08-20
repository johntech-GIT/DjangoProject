from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import mail_managers
from .models import PostCategory
from NewsPaper.NewsPortal.tasks import new_post_subscription


@receiver(m2m_changed, sender=PostCategory,)
def notify_subscribers(sender, instence, **kwargs):
    if kwargs['action'] == 'post_add':
        pass
        new_post_subscription(instence)