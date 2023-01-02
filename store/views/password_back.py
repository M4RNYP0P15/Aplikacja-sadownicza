from django.shortcuts import render, redirect
from ..forms import SetPasswordForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.query_utils import Q
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from ..tokens import account_activation_token


@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Hasło zostało zmienione")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    form = SetPasswordForm(user)
    return render(request, 'password/password_reset_confirm.html', {'form': form})

def password_reset_request(request):
    if request.user.is_authenticated:
        return redirect('store:homepage')

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Prośba o zmianę hasła"
                message = render_to_string("password/template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        <h2>Wysłano prośbę o zmianę hasła</h2><hr>
                        <p>
                            Wysłaliśmy Ci instrukcje dotyczące ustawienia hasła, jeśli konto istnieje na podany przez Ciebie adres e-mail.
                            Wkrótce powinieneś go otrzymać.<br>Jeśli nie otrzymałes maila, upewnij się że wprowadziłeś poprawny adres email,
                            i sprawdź folder spam.
                        </p>
                        """
                    )
                else:
                    messages.error(request, "Napotkano problem podczas wysyłania wiadomości, <b>PROBLEM SERWERA</b>")

            return redirect('store:homepage')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'To pole jest wymagane.':
                messages.error(request, "Musisz wykonać test reCAPTCHA.")
                continue
    
    
    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="password/password_reset.html", 
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    return redirect("store:homepage")