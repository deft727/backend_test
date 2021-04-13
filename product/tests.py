
from decimal import Decimal
from django.test import TestCase,Client,RequestFactory
from .models import Product,Category,Like,Comment
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
from django.urls import reverse
from .forms import LikeForm
from .views import CartView,cart_add
from unittest import mock
from cart.cart import Cart
from django.conf import settings

User = get_user_model()


class ShopTesCases(TestCase):
    
    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser',password='password',email='test@gmail.com')
        self.category = Category.objects.create(name='test_category',slug='test_category')
        image= tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.product = Product.objects.create(
            category=self.category,
            status='base',
            name='testproduct',
            slug='testproduct',
            image =image,
            price = Decimal('50.00'),
            description = 'description product test'
        )
        self.like = Like.objects.create(product=self.product,user=self.user)
        self.comment = Comment.objects.create(product=self.product,user=self.user,text='test text for comment')

