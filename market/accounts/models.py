import re

from django.contrib.auth.models import AbstractUser, UserManager
from django.db                  import models
from django.utils.safestring    import mark_safe
from django.forms.models        import model_to_dict

from unidecode                  import unidecode
from any_imagefield.models      import AnyImageField

class CompanyBookManager(models.Manager):
    def store_address(self, user, address, alias):
        data = Company.objects.as_data(address)
        query = dict(('address__%s' % (key,), value)
                     for key, value in data.items())
        candidates = self.get_queryset().filter(user=user, **query)
        candidates = candidates.select_for_update()
        try:
            entry = candidates[0]
        except IndexError:
            address = Company.objects.create(**data)
            entry = CompanyBook.objects.create(user=user, address=address, alias=alias)
        return entry


class CompanyBook(models.Model):
    user    = models.ForeignKey('User', related_name='company_book')
    company = models.ForeignKey('Company', related_name='+', unique=True)
    alias   = models.CharField(help_text='Короткое описание компании', max_length=30)

    objects = CompanyBookManager()

    class Meta:
        unique_together = ('user', 'alias')

    def __str__(self):
        return self.alias

    def count(self):
        return self.objects.all().count()

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

    def as_data(self, co):
        return model_to_dict(co, exclude=['id', 'user'])

    def are_identical(self, co1, co2):
        data1 = self.as_data(co1)
        data2 = self.as_data(co2)
        return data1 == data2

class Company(models.Model):
    company_name = models.CharField(name="company_name", max_length=256, blank=False)
    phone        = models.CharField(name="phone", max_length=256, blank=True)
    #TODO: min length for inn, kpp
    inn          = models.CharField(name="inn", max_length=10, blank=False)
    kpp          = models.CharField(name="kpp", max_length=9, blank=False)
    address      = models.TextField(name="address", max_length=256, blank=True)

    objects = CompanyManager()

    def __str__(self):
        return "%s %s" % (self.company_name, self.address)

    def __repr__(self):
        return self.phone


AbstractUser._meta.get_field('email')._unique   = True
AbstractUser._meta.get_field('email')._blank    = False
AbstractUser._meta.get_field('username')._blank = True

class UserManager(UserManager):

    def get_or_create(self, **kwargs):
        defaults = kwargs.pop('defaults', {})
        try:
            return self.get_query_set().get(**kwargs), False
        except self.model.DoesNotExist:
            defaults.update(kwargs)
            return self.create_user(**defaults), True

    def create_user(self, email, password=None, is_staff=False, is_active=True, **extra_fields):
        # Создает пользователся с данными: имя, email, пароль
        email = UserManager.normalize_email(email)
        user = self.model(email=email, is_active=is_active, is_staff=is_staff, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        return self.create_user(email, password, is_staff=True, is_superuser=True, **extra_fields)

    def store_address(self, user, company, alias, billing=False, shipping=False):
        pass
    

class User(AbstractUser):
    phone  = models.CharField(max_length=20, blank=True)
    avatar = AnyImageField("avatar", upload_to='accounts/avatar/%Y/%m/', blank=True,  max_length=1000)
    default_company = models.ForeignKey(CompanyBook, related_name='+', null=True, blank=True, db_column="default_company",
       on_delete=models.SET_NULL)

    objects = UserManager()

    def __str__(self):
        return self.get_username()

    def get_username(self):
        return self.first_name



