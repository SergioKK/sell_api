from django.contrib import admin
from sell_api.models import Category, Items, Subcategory

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Items)