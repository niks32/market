from . import SessionCart, CART_SESSION_KEY


class CartMiddleware(object):
    """
    Сохраняет обект корзины в сессии
    """
    @staticmethod
    def process_request(request):
        try:
            cart_data = request.session[CART_SESSION_KEY]
            cart = SessionCart.from_storage(cart_data)
        except KeyError:
            cart = SessionCart()
        setattr(request, 'cart', cart)

    @classmethod
    def process_response(self, request, response):
        if hasattr(request, 'cart') and request.cart.modified:
            request.cart.modified = False
            to_session = request.cart.for_storage()
            request.session[CART_SESSION_KEY] = to_session
        return response