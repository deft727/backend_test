from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel
from django_resized import ResizedImageField

from django.conf import settings


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=200)
    slug = models.SlugField(_('Slug'), unique=True)

    PARAMS = Choices(
        ('following', 'following'),
        ('price_to', 'price_to'),
        ('price_from', 'price_from'),
    )

    def get_absolute_url(self):
        return reverse('products:category_detail',kwargs={'slug':self.slug})

    def __str__(self):
        return self.name


class Product(models.Model):

    BASE_STATUS='base'
    STANDART_STATUS='standard'
    PREMIUM_STATUS= 'premium'

    GRADE_CHOICES = (
    (BASE_STATUS, _('base')),
    (STANDART_STATUS, _('standard')),
    (PREMIUM_STATUS, _('premium')),
    )

    status =models.CharField(_('status'),max_length=100,choices=GRADE_CHOICES, default=BASE_STATUS)
    name = models.CharField(_('Name'), max_length=200)
    slug = models.SlugField(_('Slug'),unique=True)
    image = ResizedImageField(size=[500, 300], upload_to='products/%Y/%m/%d/',crop=['middle', 'center'],verbose_name='Image')
    price = models.DecimalField(_('Price'), decimal_places=2, max_digits=9)
    description = models.TextField(_('Description'), blank=True)
    category = models.ForeignKey(Category, related_name='products',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    order_num = models.IntegerField(default=0)
    is_popular = models.BooleanField(default=False,verbose_name='popular?')

    class Meta:
        ordering = ('-created', )

    def get_absolute_url(self):
        return reverse('products:product_detail',kwargs={'slug':self.slug})

    def __str__(self):
        return self.name


class Like(TimeStampedModel):
    product = models.ForeignKey(Product, related_name='likes',on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='likes',on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        unique_together = (('product', 'user'), ('product', 'ip'))

    def __str__(self):
        return '{} from {}'.format(self.product, self.user or self.ip)


class Comment(TimeStampedModel):

    class Meta:
        ordering = ('-pk', )

    product = models.ForeignKey(Product, related_name='comments',on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='comments',on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(blank=True, null=True)
    text = models.TextField(_('Comment'),max_length=500,help_text='maximum 500 characters ')

    def __str__(self):
        return 'comment from {}'.format(self.user or self.ip)
    
