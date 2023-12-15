from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from .models import Blog
from user_profile.models import Follow, User
from notification.models import Notification



#for email notification
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

@receiver(post_save, sender=Blog)
def send_notification_on_new_blog(sender, instance, created, **kwargs):
    if created:
        subject = 'New Blog Post Notification'
        user = instance.user  # Assuming there's a ForeignKey named 'user' in your Blog model
        user_name = user.get_full_name() if user.get_full_name() else user.username
        user_email = user.email

        message = f'A new blog post titled "{instance.title}" has been created by {user_name} ({user_email}).\n\n'
        message += f'View the blog post: {settings.BASE_URL}{reverse("blog_details", args=[instance.slug])}'
        
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.ADMIN_EMAIL_ADDRESS]  # Replace with your admin email address

        send_mail(subject, message, from_email, recipient_list)

# @receiver(post_save, sender=Blog)
# def send_notification_on_new_blog(sender, instance, created, **kwargs):
#     if created:
#         subject = 'New Blog Post Notification'
#         message = f'A new blog post titled "{instance.title}" has been created.\n\n'
#         message += f'View the blog post: {settings.BASE_URL}{reverse("blog_details", args=[instance.slug])}'
#         from_email = settings.DEFAULT_FROM_EMAIL
#         recipient_list = [settings.ADMIN_EMAIL_ADDRESS]  # Replace with your admin email address

#         send_mail(subject, message, from_email, recipient_list)












@receiver(post_save, sender=Blog)
def send_notification_to_followers_when_blog_created(instance,created,*args, **kwargs):
    if created:
        followers = instance.user.followers.all()
        for data in followers:
            follower = data.followed_by
            if not data.muted:
                Notification.objects.create(
                    content_object = instance,
                    user = follower,
                    text =  f"{instance.user.username} posted a new blog",
                    notification_types = "Blog"
                )

@receiver(post_save, sender=Follow)
def send_notification_to_user_when_someone_followed(instance,created,*args, **kwargs):
    if created:
        followed = instance.followed       
        if not instance.muted:
            Notification.objects.create(
                content_object = instance,
                user = followed,
                text =  f"{instance.followed_by.username} started following you",
                notification_types = "Follow"
            )

@receiver(m2m_changed, sender=Blog.likes.through)
def send_notification_when_someone_likes_blog(instance, pk_set, action, *args, **kwargs):
    if action == "post_add" and pk_set:
        pk = list(pk_set)[0]
        user = User.objects.get(pk=pk)
        Notification.objects.create(
            content_object=instance,
            user=instance.user,
            text=f"{user.username} liked your blog",
            notification_types="Like"
        )


