from django import forms
from .models.products import Valve

######
### admin forms
######
class ValveAdminForm(forms.ModelForm):
    class Meta:
        model = Valve

class ProductVariantInline(forms.models.BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            if form.cleaned_data:
                count += 1
        if count < 1:
            raise forms.ValidationError('Вы должны добавить хотя бы один вариант.')
#######
### users forms
#######

#class VavleForm(AddToCartForm):
class ValveForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)


    def __init__(self, *args, **kwargs):
        super(ValveForm, self).__init__(*args, **kwargs)
        print(self)



#     size = forms.ChoiceField(choices=,  widget=forms.RadioSelect())
    #def __init__(self, *args, **kwargs):
     #   super(ShirtForm, self).__init__(*args, **kwargs)
      #  available_sizes = [
       #     (p.size, p.get_size_display()) for p in self.product.variants.all()
        #]
        #self.fields['size'].choices = available_sizes

    #def get_variant(self, clean_data):
     #   size = clean_data.get('size')
      #  return self.product.variants.get(size=size,
       #                                  product__color=self.product.color)

#staff
def get_form_class_for_product(product):
    if isinstance(product, Valve):
        return ValveForm
    raise NotImplementedError