from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import mail_managers
from .models import PostCategory
from .tasks import new_post_subscription


@receiver(m2m_changed, sender=PostCategory,)
def notify_subscribers(sender, instаnce, **kwargs):
    if kwargs['action'] == 'post_add':
        pass
        new_post_subscription(instаnce)

@receiver(post_save, sender=User,)
def notify_user_signup(sender, instаnce, **kwargs):
    if kwargs['action'] == 'post_add':
        pass
        new_post_subscription(instаnce)