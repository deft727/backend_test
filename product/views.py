from collections import OrderedDict
from datetime import timedelta
from braces.views import JSONResponseMixin, AjaxResponseMixin
from django.contrib import messages
from django.db.models import Sum, Case, When, IntegerField, Count, F, Q
from django.db.models.functions import Coalesce
from django.db import transaction
from django.http import Http404
from django.shortcuts import render,redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, FormView, TemplateView,View
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .forms import LikeForm,ReviewsForm
from .models import Category, Product, Like , Comment
from .mixins import ClientIp
# 
from common.mixins import ActiveTabMixin
from common.utils import get_ip_from_request

from django.views.generic.list import MultipleObjectMixin
from django.core.paginator import Paginator

@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    messages.add_message(request,messages.SUCCESS,'product added to cart successfully')
    return redirect("home")


@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    messages.add_message(request,messages.SUCCESS,'product deleted')
    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))


@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    messages.add_message(request,messages.SUCCESS,'quantity changed')
    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))


@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    messages.add_message(request,messages.SUCCESS,'quantity changed')
    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.add_message(request,messages.SUCCESS,'cart is empty')
    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))


class CategoryListView(ActiveTabMixin, ListView):
    model = Category
    # active_tab = 'category_list'
    template_name='category_list'
    allow_empty=False
    def get_ordered_grade_info(self):
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grade_info'] = self.get_ordered_grade_info()
        context['title']='test tasks'
        return context


class CategoryDetailView(DetailView,MultipleObjectMixin):
    model = Category
    # slug_url_kwarg = 'slug'
    PARAM_FOLLOWING = 'following'
    PARAM_PRICE_FROM = 'price_from'
    PARAM_PRICE_TO = 'price_to'
    allow_empty=False
    context_object_name='category'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        object_list = Product.objects.filter(category=self.get_object()).order_by('-pk')
        context = super(CategoryDetailView, self).get_context_data(object_list=object_list, **kwargs)
        page_number = self.request.GET.get('page',1) 
        paginator = Paginator(object_list, 1)
        page =paginator.get_page(page_number)
        context['category'] = page
        context['title']=self.get_object().name
        return context


class ProductDetailView(DetailView):
    model = Product
    slug_url_kwarg = 'slug'
    category = None
    allow_empty=False
    def get(self, request, *args, **kwargs):
        # print(self.get_object().category)
        try:
            self.category = Category.objects.get(slug=self.get_object().category.slug)
        except Category.DoesNotExist:
            raise Http404
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']=self.get_object().name
        context['form']= ReviewsForm(self.request.POST or None)
        context['popular'] = Product.objects.filter(Q(order_num__gte=1)|Q(is_popular=True),\
        ~Q(name=self.get_object().name)).order_by('order_num')[:10]
        return context


class LikeToggleView(AjaxResponseMixin, ClientIp, JSONResponseMixin, FormView):
    http_method_names = ('post', )
    form_class = LikeForm
    product = None

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        product_id = kwargs['id']
        try:
            self.product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        product_id = kwargs['id']
        product = Product.objects.get(id=product_id)

        try:
            if request.user.is_authenticated:
                exist=Like.objects.get(product__id=product_id,user=request.user) 
            else:
                exist=Like.objects.get(product__id=product_id,ip=self.get_client_ip(request))
            if exist:
                exist.delete()
        except:
            if request.user.is_authenticated:
                Like.objects.create(product=product,user=request.user)
            else:
                Like.objects.create(product=product,ip=self.get_client_ip(request))
        return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))


# class AddToCartView(AjaxResponseMixin, JSONResponseMixin, FormView):
#     http_method_names = ('post',)
#     success_url = reverse_lazy('products:cart')

#     def post(self, request, *args, **kwargs):
#         print('aasd')
#         # raise NotImplementedError


class CartView(ActiveTabMixin, TemplateView):
    active_tab = 'cart'
    template_name = 'product/cart.html'


class AddReview(ClientIp,View):
    def post(self,request,id):
        product = Product.objects.get(id=id)
        form=ReviewsForm(request.POST or None)
        if  form.is_valid():
            form=form.save(commit=False)
            if request.user.is_authenticated:
                form.user = request.user
            else:
                form.ip=self.get_client_ip(request)
            form.product=product
            form.save()
            messages.add_message(request,messages.SUCCESS,'comment added')
        else:
            messages.add_message(request,messages.ERROR,'error')
        return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))


