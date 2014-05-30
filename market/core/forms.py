from django import forms
from django.contrib.auth.models import AnonymousUser


class GetPhoneForm(forms.Form):
    def __init__(self, user=None, *args, **kwargs):
        super(GetPhoneForm, self).__init__(*args, **kwargs)
        if not(type(user) is AnonymousUser):
            self.fields['name'] = forms.CharField(label=user.first_name)
        else:
            self.fields['name'] = forms.CharField(label="Кто")

    phone = forms.CharField(max_length=15, label="Телефонный номер")
    about = forms.CharField(widget=forms.Textarea, label="Тема звонка")



    #    if not user.is_authenticated():
            # Add a name field since the user doesn't have a name
            #self.fields['name'] = forms.CharField(label='Full name')



