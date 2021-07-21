from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import pre_save


@receiver(post_save, sender=User)
def updateUser(sender, instance, **kwargs):
    user = instance
    if user.email != "":
        user.username = user.email


@receiver(post_save, sender=User)
def send_email(sender, instance, created, *args, **kwargs):
    if created:
        user = instance

        subject = "Welcome to Ecommerce"
        message = f"Hi there, \n\n\n Thanks {user.username} for signing up. We're so glad you are here! \n\n \n Cheers,\n  Team E-commerce"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
