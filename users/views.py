from __future__ import absolute_import, unicode_literals
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.views.generic import View
from  django.shortcuts  import render,redirect
from .forms import RegistrationForm


class RegistrationView(View):
    def get(self,request,*args,**kwargs):
        if  request.user.is_authenticated:
            messages.add_message(request,messages.ERROR,'the user is already logged in')
            return redirect('home')
        form=RegistrationForm(request.POST or None)
        title = 'Register'
        context = {
            'title':title,
            'form':form,
        }
        return render(request,'register.html',context)
    
    def post(self,request,*args,**kwargs):
        form= RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.username=form.cleaned_data['username']
            new_user.email=form.cleaned_data['email']
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user= authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            login(request,user)
            messages.add_message(request,messages.SUCCESS,'registration completed successfully')
            return redirect('home')
        else:
            messages.add_message(request,messages.ERROR,'Error, try again')
        context={'form':form,}
        return render(request,'register.html',context)


class ProfileView(View):
    def get (self,request,*args,**kwargs):
        if not  request.user.is_authenticated:
            messages.add_message(request,messages.ERROR,'you need register')
            return redirect('registration')
        customer = request.user
        title = 'profile: '+ request.user.username

        return render(request,'product/profile.html',{'title':title,
        'customer':customer,
 })

