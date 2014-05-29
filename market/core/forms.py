from django import forms


class GetPhoneForm(forms.Form):
    name = forms.CharField(max_length=20, label="Имя")
    phone = forms.CharField(max_length=15, label="Телефонный номер")
    about = forms.CharField(widget=forms.Textarea, label="Тема звонка")

