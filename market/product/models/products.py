from django.db    import models

from .core_models import Product
from .variants    import ProductVariant, StockedProduct

class Valve(Product):

    class Meta:
        app_label           = 'product'
        verbose_name        = u'Задвижка'
        verbose_name_plural = u'Задвижки'


class ValveVariant(ProductVariant, StockedProduct):

    product = models.ForeignKey(Valve, related_name='variants')
    dn = models.CharField(help_text="Dn", max_length=8)

    class Meta:
        app_label = 'product'