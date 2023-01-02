from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.contrib import messages
# from forms import UserUpdateForm
from ..forms import UserUpdateForm

def profile(request, username):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()
            messages.success(request, f'{user_form}, Twój profil został zmodyfikowany!')
            return redirect('profile', user_form.username)

        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        return render(request, 'profile.html', context={'form': form})

    return redirect("store:homepage")