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
            return redirect('store:login')
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
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Twoje hasło zostało ustawione. Możesz się <b>zalogować</b>.")
                return redirect('store:homepage')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'password/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link wygasł")

    messages.error(request, 'Coś poszło nie tak, powracanie do strony głównej')
    return redirect("store:homepage")

def activateEmail(request, user, to_email):
    mail_subject = 'Aktywuj swoje konto.'
    message = render_to_string('template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    print(message)
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Szanowny <b>{user}</b>, proszę sprawdzić swoją pocztę <b>{to_email}</b> i wcisnąć w \
            otrzymany link aktywacyjny w celu potwierdzenia i zakończenia procesu rejestracji. <b>Uwaga:</b> Sprawdź folder spam.')
    else:
        messages.error(request, f'Wystąpił problem podczas wysyłania maila {to_email}, sprawdź czy został wpisany poprawnie.')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Dziękujemy za potwierdzenie adresu email. Możesz zalogować się na swoje konto.")
        return redirect('store:login')
    else:
        messages.error(request, "Nie poprawny link aktywacyjny!")
    return redirect('store:homepage')