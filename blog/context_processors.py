from .models import Category,Site,Blog, Ugv_Ad

def get_all_categories(request):
    categories = Category.objects.all()[:20]
    category_counts = []
    for category in categories:
        blog_count = Blog.objects.filter(category=category).count()
        if blog_count > 0:  # Only include non-empty categories
            category_counts.append({'category': category, 'blog_count': blog_count})
    context = {
        "categories":categories,
        "category_counts": category_counts,
    }
    return context

def site_info(request):
    site = Site.objects.all()
    context = {
        "site":site,
    }
    return context


def ugv_ads(request):   
    latest_ad = Ugv_Ad.objects.all()
    context =  {
        'latest_ad': latest_ad,
    }
    return context