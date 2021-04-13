# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, include
from product import views
from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    path('',CategoryListView.as_view(),name = 'category_list'),
    path('cart/',CartView.as_view(), name='cart'),
    path('product_like/<int:id>/',LikeToggleView.as_view(), name='like_toggle'),
    path('product/<str:slug>/',ProductDetailView.as_view(), name='product_detail'),    
    path('category_detail/<str:slug>/',CategoryDetailView.as_view(),name='category_detail'),
    path('add_comment/<int:id>/',AddReview.as_view(),name='add_comment'),
    # here you can see sessions cart urls
    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
]
