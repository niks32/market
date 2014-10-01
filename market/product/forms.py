from django import forms
from .models.products import Valve
from market.cart.forms import AddToCartForm

import sys


class ValveAdminForm(forms.ModelForm):
    """
    Admin form
    """
    class Meta:
        model = Valve


class ProductVariantInline(forms.models.BaseInlineFormSet):
    """
    Checker not none variant
    """
    def clean(self):
        count = 0
        for form in self.forms:
            if form.cleaned_data:
                count += 1
        if count < 1:
            raise forms.ValidationError('Вы должны добавить хотя бы один вариант.')


class ValveForm(AddToCartForm):
    """
    Форма заказа
    """
    dn = forms.ChoiceField(widget=forms.RadioSelect, label='Dn')
    #price = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(ValveForm, self).__init__(*args, **kwargs)

        main_choices = []
        for p in self.product.variants.all():
            print(p.dn)
            main_choices.append([p.name, p.dn])

        self.fields['dn'].choices = main_choices

    def get_variant(self, clean_data):
        dn = clean_data.get('dn')

        return self.product.variants.get(dn=dn)

    #def get_variant(self, clean_data):
     #   size = clean_data.get('size')
      #  return self.product.variants.get(size=size,
       #                                  product__color=self.product.color)


#staff
def get_form_class_for_product(product):
    if isinstance(product, Valve):
        return ValveForm
    raise NotImplementedError