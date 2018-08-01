from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class CustomUserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class DocumentType(models.Model):
    name = models.CharField(max_length=128, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'doc_types'

    def __str__(self):
        return self.name


class AccessGroup(models.Model):
    name = models.CharField(max_length=100)
    doctypes = models.ManyToManyField(DocumentType)

    class Meta:
        db_table = 'groups'


class User(AbstractUser):
    patronymic = models.CharField(_('patronymic'), max_length=30, blank=True)
    date_changed = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(AccessGroup, models.SET_NULL, null=True)

    objects = CustomUserManager()

    def get_full_name(self):
        full_name = '%s %s %s' % (self.last_name, self.first_name, self.patronymic)
        return full_name.strip()

    @property
    def available_types(self):
        if self.group is None:
            return None
        return self.group.doctypes.values_list('id', flat=True)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        db_table = 'users'


class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name

    @property
    def url(self):
        return reverse('shop:product', args=[self.id])


class Store(models.Model):
    name = models.CharField(max_length=128, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stores'

    def __str__(self):
        return self.name

    @property
    def url(self):
        return reverse('shop:store', args=[self.id])


class Document(models.Model):
    store = models.ForeignKey(Store, models.CASCADE, related_name='documents')
    doc_type = models.ForeignKey(DocumentType, models.CASCADE, related_name='documents')
    doc_date = models.DateTimeField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT, related_name='documents')
    date_created = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    @property
    def products_list(self):
        doc_products = DocumentProduct.objects.filter(document_id=self.id).order_by('product__name')
        return ', '.join(['%s (%s)' % (p.product.name, p.number) for p in doc_products])

    def __str__(self):
        return 'with type %s for %s from %s' % (self.doc_type, self.store, self.doc_date)

    class Meta:
        db_table = 'documents'


class DocumentProduct(models.Model):
    document = models.ForeignKey(Document, models.CASCADE, 'products')
    product = models.ForeignKey(Product, models.CASCADE)
    number = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'doc_products'
        unique_together = ("document", "product")
