from django.contrib import admin
from product.models import Category, Product, Like , Comment
from django import forms
from ckeditor.widgets import CKEditorWidget

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# class MyUserAdmin(BaseUserAdmin):
#     # ....
#     list_filter = BaseUserAdmin.list_filter + ('groups__name',)
#     # ....
#     admin.site.unregister(User)
#     admin.site.register(User, MyUserAdmin)
# @admin.register(Product)



# class UserActiveAdmin(admin.ModelAdmin):
#     list_filter =(
#         ('section', TreeRelatedFieldListFilter),
#     )



class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Product
        fields = '__all__'


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':("name",)}
    form = ProductAdminForm



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':("name",)}


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product,ProductAdmin)
admin.site.register(Comment)