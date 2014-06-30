
from satchless.item import Partitioner

from . import Cart

def index(request):
    cart = Cart.for_session_cart(request.cart)
    cart_partitioner = Partitioner(cart)
    formset =