
from django.db    import models

from .core_models import Product
from .variants    import ProductVariant, StockedProduct

class Valve(Product):

    class Meta:
        app_label           = 'product'
        verbose_name        = u'Задвижку'
        verbose_name_plural = u'Задвижки'

class ValveVariant(ProductVariant, StockedProduct):

    product = models.ForeignKey(Valve, related_name='variants')

    class Meta:
        app_label = 'product'