from satchless.item import Partitioner

from django.contrib           import messages
from django.shortcuts         import  redirect
from django.template.response import TemplateResponse

from .      import Cart
from .forms import ReplaceCartLineFormSet

def index(request):
    cart = Cart.for_session_cart(request.cart)
    cart_partitioner = Partitioner(cart)
    formset = ReplaceCartLineFormSet(request.POST or None, cart=cart)
    if formset.is_valid():
        msg = 'Количества товаров были обновлены'
        messages.success(request, msg)
        formset.save()
        return redirect('cart:index')
    return TemplateResponse(request, 'cart/index.html', {
            'cart': cart_partitioner,
            'formset': formset  })