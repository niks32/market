from django import forms
from .models import GetCallModel



class GetPhoneForm(forms.ModelForm):

    class Meta:
        model = GetCallModel
        fields = ['name', 'phone', 'quest']

    def __init__(self, user=None, *args, **kwargs):
        super(GetPhoneForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(label="Имя", max_length=30, required=True)
        self.fields['phone'] = forms.CharField(label="Телефон", max_length=30, required=True)
        if user.is_authenticated():
            self.fields['name'].widget.attrs['value'] = user.first_name
            self.fields['phone'].widget.attrs['value'] = user.phone

