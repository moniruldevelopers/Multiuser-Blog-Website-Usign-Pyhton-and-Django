from django.urls import path
from .views import *
urlpatterns = [
path('', home, name = 'home'),
path('blogs/', blogs, name = 'blogs'),
path('category_blogs/<str:slug>/', category_blogs, name ='category_blogs'),
path('tag_blogs/<str:slug>/', tag_blogs, name ='tag_blogs'),
path('blog/<str:slug>/', blog_details, name ='blog_details'),
path('add_reply/<int:blog_id>/<int:comment_id>/', add_reply, name ='add_reply'),
path('like_blog/<int:pk>/',like_blog, name='like_blog'),
path('search_blogs/',search_blogs, name='search_blogs'),
path('my_blogs/', my_blogs, name='my_blogs'),
path('add_blog/', add_blog, name='add_blog'),
path('update_blog/<str:slug>/', update_blog, name='update_blog'),
path('custom_404/',custom_404, name='custom_404'),
path('about/',about, name='about'),
path('contact/',contact, name='contact'),
#wishlist url
path('add_to_wishlist/<slug:slug>/', add_to_wishlist, name='add_to_wishlist'),
path('wishlist/', wishlist_view, name='wishlist'),
path('remove_from_wishlist/<slug:slug>/', remove_from_wishlist, name='remove_from_wishlist'),
#reprot blog 
path('blog/report/<slug:slug>/', report_blog, name='report_blog'),
path('deleted_blogs/', deleted_blogs, name='deleted_blogs'),


#for chart
path('user_blog_views_chart/', user_blog_views_chart, name='user_blog_views_chart'),
path('line_chart/', line_chart, name='line_chart'),  # New URL for the line chart

path('top-bloggers/', top_bloggers_view, name='top_bloggers_view'),

]

handler404 = custom_404