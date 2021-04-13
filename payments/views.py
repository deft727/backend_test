import json
import stripe
from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView,View
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.db import transaction
from django.contrib.auth import get_user_model
from .forms import OrderPayForm,OrderForm
from .models import Order, Customer
from cart.cart import Cart

User = get_user_model()


class MakeOrderView(View):
    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        cart = Cart(request)
        cart=cart.cart

        if bool(cart) is False:
            return redirect('home')

        title='checkout'
        context = {
            'title':title,
            'form': form
        }
        return render(request, 'checkout.html', context)


    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        cart = Cart(request)
        cartdetail=cart.cart
        # name = str(self.request.session.session_key)
        customer = Customer.objects.get_or_create(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = request.user.customer
            price = 0
            for key,value in cartdetail.items():
                price+= int(value['price'][:-3])
            new_order.amount= price
            new_order.save()
            cart.clear()
            messages.add_message(request,messages.SUCCESS,'thanks for order')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class OrderPayView(FormView):
    template_name = 'payments/order_pay.html'
    form_class = OrderPayForm
    success_url = reverse_lazy('payments:order_list')

    @method_decorator([login_required, ])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class OrderListView(ListView):
    model = Order
    template_name = 'payments/order_list.html'
    @method_decorator([login_required, ])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)



class OrderDetailView(DetailView):
    model = Order
    template_name = 'payments/order_detail.html'
    @method_decorator([login_required, ])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
