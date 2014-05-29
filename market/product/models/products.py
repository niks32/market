
from django.db    import models

from .core_models import Product
from .variants    import ProductVariant, StockedProduct

class Valve(Product):

    text = models.TextField(verbose_name="text", max_length=100)
    class Meta:
        app_label           = 'product'
        verbose_name        = u'Задвижку'
        verbose_name_plural = u'Задвижки'


class ValveVariant(ProductVariant, StockedProduct):

    text    = models.TextField(verbose_name="qwe", max_length=100)
    product = models.ForeignKey(Valve, related_name='variants')

    class Meta:
        app_label = 'product'