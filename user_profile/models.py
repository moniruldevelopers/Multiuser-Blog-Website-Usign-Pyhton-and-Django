from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

#blog banner remove 
from django.utils.deconstruct import deconstructible
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db.models.signals import pre_delete,pre_save
from django.dispatch import receiver
# validity
from django.core.validators import FileExtensionValidator 
#img convert
from PIL import Image, ImageFilter
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile


class User(AbstractUser):
    email = models.EmailField(
        max_length = 150,
        unique = True,
        error_messages={
            'unique':"The email must be unique for create ",
        } 
    )
    profile_image = models.ImageField(        
        null = True,
        blank = True,        
        upload_to='users_images/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png','jpeg'])]        
    )
    followers = models.ManyToManyField("Follow")

    REQUIRED_FIELDS = ["email"]
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    def get_profile_picture(self):
        url=""
        try:
            url = self.profile_image.url
        except:
            url = ""
        return url

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Check if the image is larger than 3MB
        if self.profile_image and self.profile_image.size > 3 * 1024 * 1024:
            img = Image.open(self.profile_image.path)
            output_io = BytesIO()

            # Resize the image to a reasonable size (you can adjust this)
            img = img.resize((300, 300))

            # Save the image to the BytesIO buffer
            img.save(output_io, format='JPEG', quality=70)
            output_io.seek(0)

            # Update the profile_image field with the resized and compressed image
            self.profile_image = InMemoryUploadedFile(output_io, 'ImageField', "%s.jpg" % self.profile_image.name.split('.')[0], 'image/jpeg', output_io.tell(), None)
            super().save(*args, **kwargs)













class Follow(models.Model):
    followed = models.ForeignKey(
        User,
        related_name = 'user_followers',
        on_delete = models.CASCADE
    )
    followed_by = models.ForeignKey(
        User,
        related_name='user_follows',
        on_delete = models.CASCADE
    )
    muted = models.BooleanField(default = False)
    created_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.followed_by.username} started following {self.followed.username}"