from django.conf                    import settings
from django.core.urlresolvers       import reverse
from django.contrib                 import messages
from django.utils                   import timezone
from django.contrib.auth            import get_user_model, REDIRECT_FIELD_NAME
from django.contrib.auth            import (logout as auth_logout, login as auth_login)
from django.contrib.auth.views      import password_change
from django.shortcuts               import redirect, resolve_url, get_object_or_404
from django.template.response       import TemplateResponse
#from django.utils.http             import is_safe_url
from django.contrib.auth.forms      import AuthenticationForm
from django.contrib.sites.models    import get_current_site
from django.contrib.auth.decorators import login_required

from . import forms
from ..accounts.models              import CompanyBook

#decorators
from django.views.decorators.cache   import never_cache
from django.views.decorators.csrf    import csrf_protect
from django.views.decorators.debug   import sensitive_post_parameters


User = get_user_model()
now  = timezone.now()

@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request):
    if request.method == "POST":
        form = forms.LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            #company_book = get_object_or_404(CompanyBook, user=user)
            messages.success(request, "Мы рады приветствовать Вас на нашем сайте, %s" % user)
            return redirect("account:details")
    else:
        form = forms.LoginForm(request)

    current_site = get_current_site(request)
    context = {
        'form': form,
        'site': current_site,
        'site_name': current_site.name,
    }
    return TemplateResponse(request, template='registration/login.html', context=context)

def logout(request):
    auth_logout(request)
    messages.info(request, 'Вы вышли')
    return redirect("account:details")

def register(request):
    if request.method =='POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            email    = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create_user( email.lower(),
                                             email.lower(),
                                             password)
            #ToDo: организовать активацию
            #user.is_active  = False
            user.first_name = form.cleaned_data['first_name']
            user.last_name  = form.cleaned_data['last_name']
            user.save()
            messages.info(request,"Регистрация прошла успешно: Email:"+email+" Пароль: "+password)
            return redirect("account:details")
    else:
        form = forms.RegistrationForm()
    return TemplateResponse(request, 'registration/new_user.html', {'form':form })


@login_required( None , None, "/profile/login" )
def change_password(request):
    msg = 'Информация: используйте сложный пароль. <a href="http://8pw.ru/</b>" target="_blank">Генератор паролей</a>'
    messages.info(request, msg, fail_silently=True)
    return password_change(request,
                           template_name="registration/change_password.html",
                           post_change_redirect=reverse('profile:details'))


def request_email_change(request):
    msg = "Данный сервис в данный момент находится в разработке."
    messages.info(request, msg)
    form = forms.RequestEmailConfirmationForm()

    #temporary
    form.fields['email'].widget.attrs['value'] = 'billy@microsoft.com'
    form.fields['email'].widget.attrs['readonly'] = True

    return TemplateResponse(request, 'registration/request_email_confirmation.html', { 'form':form })