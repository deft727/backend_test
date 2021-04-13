from django import template
from product.models import Product,Like
from datetime import date,timedelta
from django.utils import timezone
from django.db.models import Q,Count
from django.db.models import Max

register = template.Library()

@register.simple_tag()
def get_likes_products():
    return Like.objects.filter(product__gte=1).distinct('product')[:10]
    # .annotate(like_count=Count('product')).order_by('-like_count')

@register.simple_tag()
def get_arrival_products():
    d=date.today()-timedelta(days=7)
    return Product.objects.filter(created__gte=d)


@register.simple_tag()
def get_choice_week_products():
    # order or popular
    return Product.objects.filter(Q(order_num__gte=1)|Q(is_popular=True)).order_by('order_num')


