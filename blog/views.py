from django.shortcuts import render, redirect, get_object_or_404 
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from .models import *
from .forms import TextForm, AddBlogForm ,ContactForm, ReportForm
from django.core import paginator
from django.db.models import Q
from django.contrib import messages
from django.utils.text import slugify



def share_page(request):
    # Your logic to retrieve data or context for the page goes here
    context = {
        'page_data': 'Your page data goes here',
    }
    return render(request, 'share_page.html', context)



#wish list view
@login_required(login_url='login')
def add_to_wishlist(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)    
    wishlist.blogs.add(blog)
    messages.success(request, "You saved this blog in your account ")
    return redirect('blog_details', slug=slug)

@login_required(login_url='login')
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)        
    return render(request, 'wishlist.html', {'wishlist': wishlist})


@login_required(login_url='login')
def remove_from_wishlist(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist.remove_from_wishlist(blog)   
    messages.error(request, "Deleted Saved blogs") 
    return redirect('wishlist')
#wish list view 



# Create your views here.
def home(request):  
    blogs = Blog.objects.order_by('-created_date')
    most_liked = Blog.objects.order_by('-likes')[:15]    
    populars = Blog.objects.order_by('-views')[:15]
    tags = Tag.objects.order_by('-created_date')[:15]  
    context = {
        'blogs': blogs,
        'tags':tags, 
        'populars': populars,  
        'most_liked': most_liked,       
    }
    return render(request, 'home.html',context)


    

   



def blogs(request):
    queryset = Blog.objects.order_by('-created_date')
    tags = Tag.objects.order_by('-created_date')[:15]
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset,50) 
    populars = Blog.objects.order_by('-views')[:15]    


    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context  = {
        'blogs':blogs,
        "tags":tags,
        "paginator":paginator,
        "populars": populars,
      
    }

    return render(request, 'blogs.html', context)



def category_blogs(request, slug):
    category = get_object_or_404(Category, slug = slug)
    queryset = category.category_blogs.all().order_by('-created_date')  # Order by creation date in descending order
    populars = Blog.objects.order_by('-views')[:15] 
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset,15)

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    tags = Tag.objects.order_by('-created_date')[:5]
    all_blogs = Blog.objects.order_by('-created_date')[:5]

    context = {
        "blogs":blogs,
        "tags":tags,
        "paginator":paginator,
        "all_blogs":all_blogs,
        "populars":populars,
    }
    return render(request, 'category_blogs.html', context)



def tag_blogs(request, slug):
    tag = get_object_or_404(Tag, slug = slug)
    queryset = tag.tag_blogs.all().order_by('-created_date')
    populars = Blog.objects.order_by('-views')[:15]    


    page = request.GET.get('page', 1)
    paginator = Paginator(queryset,2)

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    tags = Tag.objects.order_by('-created_date')[:5]
    all_blogs = Blog.objects.order_by('-created_date')[:5]

    context = {
        "blogs":blogs,
        "tags":tags,
        "paginator":paginator,
        "all_blogs":all_blogs,
        "populars":populars
    }
    return render(request, 'tag_blogs.html', context)
 
def blog_details(request,slug):
    form = TextForm()
    blog = get_object_or_404(Blog, slug = slug)
    populars = Blog.objects.order_by('-views')[:15]    
    category = Category.objects.get(id=blog.category.id)
    related_blogs = category.category_blogs.all()
    tags = Tag.objects.order_by('-created_date')[:5]
    
    blog.views += 1
    blog.save()

    liked_by = request.user in blog.likes.all()
    if request.method == "POST" and request.user.is_authenticated:
        form = TextForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                user = request.user,
                blog = blog,
                text = form.cleaned_data.get('text')
            )
            # return redirect('blog_details', slug=slug) previus code is 
            return redirect(reverse('blog_details', kwargs={'slug': slug}))
    
    context = {
        "blog":blog,
        "related_blogs":related_blogs,
        "tags":tags,
        "form":form,
        "liked_by":liked_by,
        "populars": populars
    }
    return render(request, 'blog_details.html', context)




@login_required(login_url='login')
def add_reply(request, blog_id, comment_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():            
            comment = get_object_or_404(Comment, id=comment_id)
            Reply.objects.create(
                user = request.user,
                comment=comment,
                text =form.cleaned_data.get('text') 
            )
    return redirect('blog_details', slug=blog.slug)


@login_required(login_url='login')
def like_blog(request, pk):
    context = {}
    blog = get_object_or_404(Blog, pk=pk)
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
        context['liked'] = False
        context['like_count'] = blog.likes.all().count() # Corrected line
    else:
        blog.likes.add(request.user)
        context['liked'] = True
        context['like_count'] = blog.likes.all().count() # Corrected line
    return JsonResponse(context, safe=False)











def search_blogs(request):
    search_key = request.GET.get('search', None)
    populars = Blog.objects.order_by('-views')[:15]    

    recent_blogs = Blog.objects.order_by('-created_date')
    tags = Tag.objects.order_by('-created_date')[:15]

    if search_key:
        blogs = Blog.objects.filter(
            Q(title__icontains=search_key)|
            Q(category__title__icontains=search_key)|
            Q(user__username__icontains=search_key)|
            Q(tags__title__icontains=search_key)
        ).distinct()
        #Paginate the blogs
        blogs = blogs.order_by('-created_date')#new added 
        page = request.GET.get('page', 1)
        paginator = Paginator(blogs, 50)
        #   # Show 10 blogs per page
      
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)
        context ={
            "blogs":blogs,
            "tags":tags,
            "recent_blogs":recent_blogs,
            "search_key":search_key,
            "populars": populars,
            
        }
        return render(request, 'search.html', context)
    else:
        return redirect('home')

   
    

@login_required(login_url='login')
def my_blogs(request):
    queryset = request.user.user_blogs.all().order_by('-created_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset,6)
    delete  = request.GET.get('delete', None)
    if delete:
        blog = get_object_or_404(Blog, pk=delete)
        if request.user.pk != blog.user.pk:
            return redirect('home')
        blog.delete()
        messages.success(request, "your blog has been deleted !")
        return redirect('my_blogs')

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {
        "blogs":blogs,

        "paginator":paginator,
  
    }
    return render(request, 'my_blogs.html',context)



@login_required(login_url='login')
def add_blog(request):
    form = AddBlogForm()
    if request.method == "POST":
        form = AddBlogForm(request.POST, request.FILES)
        if form.is_valid():
            tags = request.POST['tags'].split(',')
            user = get_object_or_404(User, pk=request.user.pk)
            category = get_object_or_404(Category, pk=request.POST['category'])
            blog = form.save(commit=False)
            blog.slug = slugify(blog.title)
            blog.user = user
            blog.category =category
            blog.save()
            for tag in tags:
                tag_input = Tag.objects.filter(
                    title__iexact = tag.strip(),
                    slug = slugify(tag.strip())
                )
                if tag_input.exists():
                    t = tag_input.first()
                    blog.tags.add(t)
                else:
                    if tag != '':
                        new_tag = Tag.objects.create(
                            title=tag.strip(),
                            slug = slugify(tag.strip())
                        )
                        blog.tags.add(new_tag)
            messages.success(request, "Blog Added successfully")
            return redirect('blog_details', slug=blog.slug)
        else:
            print(form.errors)

    context ={
        "form": form,
    }
    return render(request, 'add_blog.html', context)




@login_required(login_url='login')
def update_blog(request,slug):  
    blog = get_object_or_404(Blog, slug=slug)

    form = AddBlogForm(instance=blog)
    if request.method == "POST":
        form = AddBlogForm(request.POST, request.FILES, instance=blog)

        if form.is_valid():
            if request.user.pk != blog.user.pk:
                return redirect('home')
            tags = request.POST['tags'].split(',')
            user = get_object_or_404(User, pk=request.user.pk)
            category = get_object_or_404(Category, pk=request.POST['category'])
            blog = form.save(commit=False)
            blog.user = user
            blog.category =category
            blog.save()
            for tag in tags:
                tag_input = Tag.objects.filter(
                    title__iexact = tag.strip(),
                    slug = slugify(tag.strip())
                )
                if tag_input.exists():
                    t = tag_input.first()
                    blog.tags.add(t)
                else:
                    if tag != '':
                        new_tag = Tag.objects.create(
                            title=tag.strip(),
                            slug = slugify(tag.strip())
                        )
                        blog.tags.add(new_tag)
            messages.success(request, "Blog Updated successfully")
            return redirect('blog_details', slug=blog.slug)
        else:
            print(form.errors)

    context ={
        "form": form,
        "blog": blog,
    }
    return render(request, 'update_blog.html', context)

    
def custom_404(request, exception):
    return render(request, '404.html', status=404)

def about(request):
    teams  = OurTeam.objects.order_by('-created_date')
    context = {
        "teams": teams,
    }
 
    return render(request, 'about.html', context)

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact Form submitted successfully")
            return redirect('contact')
        else:
            messages.error(request, "Something wrong to send message")
    else:
        form = ContactForm()
    context = {
        "form": form,
    }  
    return render(request, 'contact.html', context)




#blog report 
@login_required(login_url='login')
def report_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.blog = blog
            report.user = request.user
            report.save()
            messages.success(request, "Report submitted successfully, We will review it asp !")
            return redirect('report_blog', slug=blog.slug)
    else:
        form = ReportForm()

    return render(request, 'report_blog.html', {'form': form, 'blog': blog})



#for delete  blog view  
@login_required
def deleted_blogs(request):
    # Fetch deleted blogs for the current user
    deleted_blogs = BlogTrash.objects.filter(user=request.user).order_by('-deleted_at')
    return render(request, 'deleted_blogs.html', {'deleted_blogs': deleted_blogs})




