from django.shortcuts import redirect

def not_logged_in_required(view_fuction):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_fuction(request, *args, **kwargs)
    return wrapper