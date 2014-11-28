from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from setuptools.command import alias
from .models import User, Company, CompanyBook
from django  import forms
from any_imagefield.forms   import ImagePreviewField


class AdminUserAddForm(UserCreationForm):

    class Meta:
        model  = User
        fields = ("username", "email", "password1", "password2")
        exclude = []

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])



class AdminUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ["avatar"]


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        exclude = []


    company_name = forms.CharField(label="Наименование")
    phone        = forms.CharField(label="Телефон")
    inn          = forms.CharField(label="ИНН")
    kpp          = forms.CharField(label="КПП")
    address      = forms.CharField(label="Адрес", widget=forms.Textarea)


class CompanyBookForm(forms.ModelForm):

    class Meta:
        model = CompanyBook
        fields = ['alias']

    alias = forms.CharField(label="Абривиатура")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone", "avatar"]

    avatar = ImagePreviewField(label="Аватар", required=False)
    phone  = forms.CharField(label="Телефонный номер", required=False)