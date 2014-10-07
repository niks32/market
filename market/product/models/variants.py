from django.db                import models
from django.core.validators   import MinValueValidator
from django.utils.encoding    import python_2_unicode_compatible
#from django.core.urlresolvers import reverse


from django.conf              import settings
from decimal                  import Decimal
from satchless.item           import Item, StockedItem
from django_prices.models     import PriceField
from django.utils.translation import pgettext_lazy

class PhysicalProduct(models.Model):
    price = PriceField( 'price', currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=4)

    class Meta:
        abstract = True
        app_label = 'product'


class StockedProduct(models.Model, StockedItem):
    stock = models.IntegerField(u'Количество', validators=[MinValueValidator(0)], default=Decimal(1))

    class Meta:
        abstract  = True
        app_label = 'product'

    def get_stock(self):
        return self.stock


@python_2_unicode_compatible
class ProductVariant(models.Model, Item):
    name = models.CharField(u'Название', max_length=128, blank=True, default='')
    #sku = models.CharField(pgettext_lazy('Product field', 'sku'), max_length=32, unique=True) #Предопределить
    # атрибут цен для реализации каждого варианта цены

    class Meta:
        abstract  = True
        app_label = 'product'

    def __str__(self):
        return self.name or self.product.name

    def get_price_per_item(self, **kwargs):
        if self.price is not None:
            price = self.price
        else:
            price = self.product.price
        return price

    def get_absolute_url(self):
        #slug = self.product.get_slug()
        #product_id = self.product.id
        #return reverse('product:details', kwargs={'slug': slug, 'product_id': product_id})
        pass

    def as_data(self):
        return {
            'product_name': str(self),
            'product_id': self.product.pk,
            'variant_id': self.pk,
            'unit_price': str(self.get_price_per_item().gross)
        }