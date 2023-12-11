# from django.utils.text import slugify

# def generate_unique_slug(model_instance, title, update=False):
#     """
#     Generate a unique slug for a model instance based on the given title.
#     """
#     slug = slugify(title)
#     unique_slug = slug
#     counter = 1

#     ModelClass = model_instance.__class__

#     while ModelClass.objects.filter(slug=unique_slug).exclude(pk=model_instance.pk).exists():
#         if update:
#             unique_slug = f"{slug}-{counter}"
#         else:
#             unique_slug = f"{slug}-{counter}"
#             counter += 1

#     return unique_slug


#not use because function is created in model