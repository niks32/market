from django                    import forms
from django.forms              import PasswordInput
from captcha.fields            import CaptchaField
from django.contrib.auth       import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from ..accounts.models         import User as User_model

User = get_user_model()

class LoginForm(AuthenticationForm):

    username  = forms.EmailField(label="Email", error_messages={'required': 'Email все таки придется ввести'})
    password  = forms.CharField(widget=PasswordInput(), label="Пароль", error_messages={'required': 'Куда ж мы без пароля?'})
    captcha  = CaptchaField(label="Введите код")
    error_messages = {
        'invalid_login': "Уупс. Нету. Введите корректный "
                         "email / пароль.",
        'inactive': 'Ваш аккаунт временно заблокирован :(  Либо еще не активирован'
    }

    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(request=request, *args, **kwargs)
        if request:
            email = request.GET.get('email')
            if email:
                self.fields['username'].initial = email


# форма регистрации

class RegistrationForm(forms.Form):
    exclude = []
    error_messages = {
        'duplicate_username': "Пользователь с таким логином уже существует.",
        'password_mismatch': "Пароли должны совпадать.",
    }


    email = forms.EmailField(label="Email")

    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput )
    password2 = forms.CharField(label="Повторите пароль",
        widget=forms.PasswordInput,
        help_text="Здесь должны быть одинаковые пароли.")

    first_name = forms.CharField(label="Имя", required=False)
    last_name  = forms.CharField(label="Фамилия", required=False)
    phone      = forms.CharField(label="Телефонный номер", required=False)

    captcha  = CaptchaField(label="Введите код")

    #проверка уникальности
    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            user = User_model.objects.get(email=data)
        except:
            user = None

        if user:
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return data

class RequestEmailConfirmationForm(forms.Form):
    #Поля
    email = forms.EmailField()

    template = 'registration/emails/change_email.txt'

