from django.core.urlresolvers           import reverse
from django.db                          import models
from django.utils.encoding              import python_2_unicode_compatible
from django.utils.safestring            import mark_safe


from any_imagefield.models              import AnyImageField
from model_utils.managers               import InheritanceManager
from mptt.models                        import MPTTModel
from satchless.item                     import ItemRange
from unidecode                          import unidecode
import re


@python_2_unicode_compatible
class Category(MPTTModel):
    name        = models.CharField('name', max_length=128)
    slug        = models.SlugField('slug', max_length=50, unique=True)
    description = models.TextField('description', blank=True)
    picture     = AnyImageField("picture", upload_to='product/category', null=True, blank=True, max_length=1000)
    parent      = models.ForeignKey('self', null=True, related_name='children', verbose_name='parent')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:category', kwargs={ 'slug': self.slug })

    class Meta:
        app_label = 'product'
        verbose_name = u'Категоря'
        verbose_name_plural = u'Категории'

class Product(models.Model, ItemRange):
    name     = models.CharField(verbose_name='Наименование', max_length=128)
    category = models.ForeignKey('Category', verbose_name="Категория", related_name='products')
    #price    = models.DecimalField(verbose_name='Цена', name='price',max_digits=15,decimal_places=2) не работает


    desc = models.TextField(verbose_name="Короткое описание", max_length=150, blank=True )
    desc_verbose = models.TextField(verbose_name="Полное описание", max_length=1000, blank=True)

    objects  = InheritanceManager()

    def __str__(self):
        return self.name

    def __iter__(self):
        if not hasattr(self, '__variants'):
            setattr(self, '__variants', self.variants.all())
        return iter(getattr(self, '__variants'))

    def get_absolute_url(self):
        return reverse('product:details', kwargs={'slug': self.get_slug(),
                                                  'product_id': self.id})

    def get_slug(self):
        value = unidecode(self.name)
        value = re.sub(r'[^\w\s-]', '', value).strip().lower()
        return mark_safe(re.sub(r'[-\s]+', '-', value))

    class Meta:
        app_label = 'product'
        verbose_name = 'Продукция'
        verbose_name_plural = 'Продукция'

class ProductImage(models.Model):

    product  = models.ForeignKey('Product', related_name='images', null=True)
    image = AnyImageField("Изображение", upload_to='products/%Y/%m/', blank=True, null=True,  max_length=1000)

    class Meta:
        app_label = 'product'
        verbose_name = "Изображение"
        verbose_name_plural = "Изображение"

class Product_Product(models.Model):
    price = models.DecimalField(verbose_name='Cena', name=None, max_digits=10, decimal_places=2)
    # TODO price_vip

    class Meta:
        app_label = 'price'
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'


