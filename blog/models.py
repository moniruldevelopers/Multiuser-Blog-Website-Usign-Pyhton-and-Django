from django.shortcuts import reverse
from django.db import models
from django.utils.text import slugify
from user_profile.models import User
# from .slug import generate_unique_slug

from ckeditor.fields import RichTextField
import pytz
from django.utils import timezone
from django.core.validators import RegexValidator
#img convert
from PIL import Image, ImageFilter
from io import BytesIO
from django.core.files.base import ContentFile



#blog banner remove 
from django.utils.deconstruct import deconstructible
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db.models.signals import pre_delete,pre_save
from django.dispatch import receiver

# start wish list code 
class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blogs = models.ManyToManyField('Blog')

    def add_to_wishlist(self, blog):
        self.blogs.add(blog)

    def remove_from_wishlist(self, blog):
        self.blogs.remove(blog)

    def __str__(self):
        return self.user.username + "'s Wishlist"
# end wish list code 

# site start
class Site(models.Model):
    header_logo = models.ImageField(upload_to="site_info")
    footer_logo = models.ImageField(upload_to="site_info")
    site_name = models.CharField(max_length=25)
    def __str__(self):
        return self.site_name
  
# end site 


# start category
class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
# end category

# start tag
class Tag(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
# end tag

def generate_unique_slug(model_instance, title, update=False):
    """
    Generate a unique slug for a model instance based on the given title.
    """
    slug = slugify(title)
    unique_slug = slug
    counter = 1

    ModelClass = model_instance.__class__

    while ModelClass.objects.filter(slug=unique_slug).exclude(pk=model_instance.pk).exists():
        if update:
            unique_slug = f"{slug}-{counter}"
        else:
            unique_slug = f"{slug}-{counter}"
            counter += 1

    return unique_slug

@deconstructible
class UploadToPath:
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        old_instance = instance.__class__.objects.filter(pk=instance.pk).first()
        if old_instance:
            old_instance.banner.delete(save=False)
        return f"{self.path}/{filename}"

class Blog(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_blogs',
        on_delete= models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        related_name='category_blogs',
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tag_blogs',
        blank=True
    )
    likes = models.ManyToManyField(
        User,
        related_name='user_likes',
        blank=True
    )
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    views = models.PositiveIntegerField(default=0)
    banner = models.ImageField(upload_to=UploadToPath('blog_banners'))
    description = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        updating = self.pk is not None
         # Resize the image if it's larger than 2 MB
        if self.banner:
            max_size_bytes = 2 * 1024 * 1024  # 2 MB in bytes
            if self.banner.size > max_size_bytes:
                img = Image.open(self.banner)

                # Convert image to RGB mode if it has an alpha channel
                if img.mode == 'RGBA':
                    img = img.convert('RGB')

                # Resize the image maintaining the aspect ratio with antialiasing
                max_width = 1200  # Adjust the desired width
                max_height = 800  # Adjust the desired height

                try:
                    img.thumbnail((max_width, max_height), resample=Image.BICUBIC)
                except Exception as e:
                    print(f"Error during image resizing: {e}")

                # Save the resized image back to the same field with JPEG format
                buffer = BytesIO()
                img.save(buffer, format='JPEG', quality=90, optimize=True)

                # Generate a unique filename based on the updated slug
                filename = f"{slugify(self.slug)}_eblogugv.jpg"
                self.banner.save(
                    filename,
                    ContentFile(buffer.getvalue()),
                    save=False,
                )


        # Generate a unique slug based on the title
        if updating:
            self.slug = generate_unique_slug(self, self.title, update=True)
        else:
            self.slug = generate_unique_slug(self, self.title)

       
        super().save(*args, **kwargs)





#for trash
    def delete(self, *args, **kwargs):
        # Move the blog to the trash
        BlogTrash.objects.create(
            user=self.user,
            title=self.title,
            banner=self.banner,
            description=self.description
        )
        super().delete(*args, **kwargs)






@deconstructible
class UploadToPath:
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        old_instance = instance.__class__.objects.filter(pk=instance.pk).first()
        if old_instance:
            old_instance.banner.delete(save=False)
        return f"{self.path}/{filename}"

class BlogTrash(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    banner = models.ImageField(upload_to='blog_banners/', null=True, blank=True)
    description = models.TextField()
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def restore(self):
        # Perform the restore action based on your application's logic
        # For example, you might set 'is_deleted' to False or move the blog back to the original model
        # Update the restore logic according to your actual model structure
        Blog.objects.create(
            user=self.user,
            title=self.title,
            banner=self.banner,
            description=self.description
        )
        self.delete()  # Delete the restored blog from the trash


@receiver(pre_delete, sender=BlogTrash)
def delete_media_files(sender, instance, **kwargs):
    if instance.banner:
        instance.banner.delete(save=False)











class Comment(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_comments',
        on_delete= models.CASCADE

    )
    blog = models.ForeignKey(
        Blog,
        related_name='blog_comments',
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Reply(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_replies',
        on_delete= models.CASCADE

    )
    comment = models.ForeignKey(
        Comment,
        related_name='comment_replies',
        on_delete=models.CASCADE
    )
    
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text



class Ugv_Ad(models.Model):
    ad1_url = models.URLField(max_length=300, blank=True)
    ad1 = models.ImageField(upload_to="ad/", blank=True, null=True)

    ad2_url = models.URLField(max_length=300, blank=True)
    ad2 = models.ImageField(upload_to="ad/", blank=True, null=True)

    ad3_url = models.URLField(max_length=300, blank=True)
    ad3 = models.ImageField(upload_to="ad/", blank=True, null=True)

    ad4_url = models.URLField(max_length=300, blank=True)
    ad4 = models.ImageField(upload_to="ad/", blank=True, null=True)

    ad5_url = models.URLField(max_length=300, blank=True)
    ad5 = models.ImageField(upload_to="ad/", blank=True, null=True)

    ad6_url = models.URLField(max_length=300, blank=True)
    ad6 = models.ImageField(upload_to="ad/", blank=True, null=True)

    ad7_url = models.URLField(max_length=300, blank=True)
    ad7 = models.ImageField(upload_to="ad/", blank=True, null=True)

    ad8_url = models.URLField(max_length=300, blank=True)
    ad8 = models.ImageField(upload_to="ad/", blank=True, null=True)

    ad9_url = models.URLField(max_length=300, blank=True)
    ad9 = models.ImageField(upload_to="ad/", blank=True, null=True)

    ad10_url = models.URLField(max_length=300, blank=True)
    ad10 = models.ImageField(upload_to="ad/", blank=True, null=True)

    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        updated_date_bangladesh = self.updated_date.astimezone(pytz.timezone('Asia/Dhaka'))

        days = updated_date_bangladesh.day
        month = updated_date_bangladesh.strftime("%m")
        year = updated_date_bangladesh.year
        time = updated_date_bangladesh.strftime("%I.%M %p")

        return f"{days} days/{month} month/{year} {time} (Bangladesh Time)"



class OurTeam(models.Model):
    name = models.CharField(max_length = 100)
    designation = models.CharField(max_length = 50)
    fb_url  = models.URLField(max_length = 150)
    image =  models.ImageField(upload_to ='ourteam/')
    created_date = models.DateTimeField(auto_now_add =True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: '+088'. Up to 15 digits allowed."
    )
    name = models.CharField(max_length = 100)
    phone = models.CharField(validators=[phone_regex], max_length=15)
    email = models.EmailField(max_length = 50)    
    message = models.TextField(max_length=500)
    def __str__(self):
        return self.name





#for report blog 
class BlogReport(models.Model):
    PENDING = 'pending'
    REVIEWED = 'reviewed'
    RESOLVED = 'resolved'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (REVIEWED, 'Reviewed'),
        (RESOLVED, 'Resolved'),
    ]

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING) 

    def __str__(self):
        return self.reason
    def save(self, *args, **kwargs):
        # Append the blog details URL to the original reason
        blog_url = reverse('blog_details', kwargs={'slug': self.blog.slug})
        self.reason = f"{self.reason}\n\nBlog Details: {blog_url}"
        super().save(*args, **kwargs)

#for user restricted 
class RestrictedEmail(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


