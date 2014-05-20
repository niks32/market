import re

from django.contrib.auth.models import AbstractUser
from django.db                  import models
from django.utils.safestring    import mark_safe


from unidecode import unidecode



AbstractUser._meta.get_field('email')._unique = True
AbstractUser._meta.get_field('email')._blank  = False

AbstractUser._meta.get_field('username')._blank = True

class User(AbstractUser):
     avatar = models.ImageField(u'avatar', upload_to='accounts/avatar/%Y/%m/', blank=True, max_length=1000)



class CompanyBookManager(models.Manager):
    pass


class CompanyBook(models.Model):
    user    = models.ForeignKey('User', related_name='company_book')
    company = models.ForeignKey('Company', related_name='+', unique=True)
    alias   = models.CharField(help_text='Короткое описание компании', max_length=30)

    objects = CompanyBookManager()

    class Meta:
        unique_together = ('user', 'alias')

    def __str__(self):
        return self.alias

    @models.permalink
    def get_absolute_url(self):
        return ('account:company-edit',
                (),
                {'slug': self.get_slug(), 'pk': self.id})

    def get_slug(self):
        value = unidecode(self.alias)
        value = re.sub(r'[^\w\s-]', '', value).strip().lower()
        return mark_safe(re.sub(r'[-\s]+', '-', value))


class CompanyManager(models.Manager):
    pass

class Company(models.Model):
    company_name = models.CharField(name="company_name", max_length=256, blank=False)
    phone        = models.CharField(name="phone", max_length=256, blank=True)
    inn          = models.IntegerField(name="inn", blank=False)
    kpp          = models.IntegerField(name="kpp", blank=False)
    address      = models.TextField(name="address", max_length=256, blank=True)

    objects = CompanyManager()

    def __str__(self):
        return "%s %s" % (self.company_name, self.address)

    def __repr__(self):
        return self.phone
