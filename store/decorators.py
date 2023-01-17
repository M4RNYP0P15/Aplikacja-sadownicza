from django.shortcuts import redirect
from django.contrib import messages

def user_not_authenticated(function=None, redirect_url='store:homepage'):
    """
    Dekorator do sprawdzania czy uzytkownik jest zalogowany
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
                
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator

def user_is_superuser(function=None, redirect_url='/'):
    """
    Dekorator do sprawdzania czy uzytkownik jest superuser
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_superuser:
                messages.error(request, "Nie posiadasz uprawnień do przeglądania tej strony!")
                return redirect(redirect_url)
                
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator


def user_is_moderator(function=None, redirect_url='/'):
    """
    Dekorator do sprawdzania czy uzytkownik jest co najmniej moderatorem
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if (not request.user.is_superuser) or request.user.status != 'moderator':
                messages.error(request, "Nie posiadasz uprawnień do przeglądania tej strony!")
                return redirect(redirect_url)
                
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator