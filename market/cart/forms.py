from django import forms
from django.forms.formsets import BaseFormSet
from django.core.exceptions import ObjectDoesNotExist, NON_FIELD_ERRORS

from satchless.item import InsufficientStock

import logging

class QuantityField(forms.IntegerField):
    """
    Поле заказа количества
    """
    def __init__(self, *args, **kwargs):
        super(QuantityField, self).__init__(min_value=0, max_value=999,
                                            initial=1, **kwargs)


class AddToCartForm(forms.Form):
    """
    Класс импользующий экземляры продукта и корзины
    """
    quantity = QuantityField(label='Колчиство')
    error_messages = {
        'empty-stock': 'Данного продукта нет на складе',
        'variant-does-not-exists': 'Такого продукта нет.',
        'insufficient-stock': 'Невозможно. Всего %(remaining)d в наличии',
    }

    def __init__(self, *args, **kwargs):
        self.cart = kwargs.pop('cart')
        self.product = kwargs.pop('product')
        super(AddToCartForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(AddToCartForm, self).clean()
        quantity = cleaned_data.get('quantity')
        if quantity is None:
            return cleaned_data
        try:
            logging.error(cleaned_data)
            #TODO: смотреть get_variant
            product_variant = self.get_variant(cleaned_data)
        except ObjectDoesNotExist:
            msg = self.error_messages['variant-does-not-exists']
            self.add_error(NON_FIELD_ERRORS, msg)
        else:
            cart_line = self.cart.get_line(product_variant)
            used_quantity = cart_line.get_quantity if cart_line else 0
            new_quantity = quantity + used_quantity
            try:
                self.cart.check_quantity(
                    product_variant, new_quantity, None)
            except InsufficientStock as e:
                remaining = e.item.stock - used_quantity
                if remaining:
                    msg = self.error_messages['insufficient-stock']
                else:
                    msg = self.error_messages['empty-stock']
                self.add_error('quantity', msg % {'remaining': remaining})

        print(cleaned_data)
        print(self.errors)
        return cleaned_data

    def save(self):
        """
        Добавляет CartLine в Cart
        """
        product_variant = self.get_variant(self.cleaned_data)
        return self.cart.add(product_variant, self.cleaned_data['quantity'])

    def get_variant(self, cleaned_data):
        raise NotImplementedError()

    def add_error(self, name, value):
        errors = self.errors.setdefault(name, self.error_class())
        errors.append(value)


class ReplaceCartLineForm(AddToCartForm):
    """
    Замена количества в CartLine
    """
    def __init__(self, *args, **kwargs):
        super(ReplaceCartLineForm).__init__(*args, **kwargs)
        self.cart_line = self.cart.get_line(self.product)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        try:
            self.cart.check_quantity(self.product, quantity, None)
        except InsufficientStock as e:
            msg = self.error_messages['insufficient-stock']
            raise forms.ValidationError(msg % {'remaining': e.item.stock})
        return quantity

    def clean(self):
        return super(AddToCartForm, self).clean()

    def get_variant(self, cleaned_data):
        return self.product

    def save(self):
        return self.cart.add(self.product, self.cleaned_data['quantity'], replace=True)


class ReplaceCartLineFormSet(BaseFormSet):
    """
    Formset for all CartLines in the cart instance
    """

    def __init__(self, *args, **kwargs):
        self.cart = kwargs.pop('cart')
        kwargs['initial'] = [{'quantuty': cart_line.get_quantity()}
                             for cart_line in self.cart
                             if cart_line.get_quantity()]
        super(ReplaceCartLineFormSet, self).__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['cart'] = self.cart
        kwargs['product'] = self.cart[i].product
        return super(ReplaceCartLineFormSet, self)._construct_form(i, **kwargs)

    def save(self):
        for form in self.forms:
            form.save()
