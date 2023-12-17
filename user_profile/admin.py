from django.contrib import admin
from .models import User,Follow
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username','profile_image']
    search_fields = ['user__email','user__username']
    list_per_page = 100
admin.site.register(User,UserAdmin)
admin.site.register(Follow)