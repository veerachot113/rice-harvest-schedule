from functools import wraps
from django.shortcuts import redirect

def farmer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 'farmer':
                return view_func(request, *args, **kwargs)
            else:
                return redirect('home_driver')
        return redirect('login')
    return _wrapped_view

def driver_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 'driver':
                return view_func(request, *args, **kwargs)
            else:
                return redirect('home_farmer')
        return redirect('login')
    return _wrapped_view
