from django.contrib import admin
from .models import *
from rangefilter.filters import DateRangeFilter
# Register your models here.
#my customizations
admin.site.site_header = "UGV BLOG"
admin.site.site_title = "UGV BLOG ADMIN PANEL"
admin.site.index_title = "Welcome to UGV BLOG  PORTAL"







admin.site.register(RestrictedEmail)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'user_email']
    search_fields = ['title', 'user__email', 'user__username']
    list_per_page = 100

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'User Email'

    list_filter = (
        ('created_date', DateRangeFilter),  # Replace 'created_at' with the actual name of the date field in your Blog model
    )

admin.site.register(Blog, BlogAdmin)






admin.site.register(Category)
admin.site.register(Tag)



class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_email', 'text']
    search_fields = ['text', 'user__email', 'user__username']
 
    date_hierarchy = 'created_date'

    def user_email(self, obj):
        return obj.user.email if obj.user else None

    user_email.short_description = 'User Email'

admin.site.register(Comment, CommentAdmin)

class ReplyAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_email', 'text']
    search_fields = ['text', 'user__email', 'user__username']
 
    date_hierarchy = 'created_date'

    def user_email(self, obj):
        return obj.user.email if obj.user else None

    user_email.short_description = 'User Email'
admin.site.register(Reply, ReplyAdmin)


admin.site.register(Site)

admin.site.register(Ugv_Ad)
admin.site.register(OurTeam)

admin.site.register(Wishlist)

#report blog
class BlogReportAdmin(admin.ModelAdmin):
    list_display = ['reason','blog','user', 'status']
admin.site.register(BlogReport,BlogReportAdmin)


#trash
@admin.register(BlogTrash)
class BlogTrashAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'user_email', 'deleted_at']
    search_fields = ['title', 'user__username']
    date_hierarchy = 'deleted_at'

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'User Email'




@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'name', 'message']

