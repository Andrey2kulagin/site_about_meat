from django.contrib import admin
from .models import Product, Application, UserAdditionalInfo, GoodsInShoppingCart, ProductCategories, Order, OrderItems
from django.contrib.sessions.models import Session
admin.site.register(Product)
admin.site.register(Application)
admin.site.register(UserAdditionalInfo)
admin.site.register(Session)
admin.site.register(GoodsInShoppingCart)
admin.site.register(ProductCategories)
admin.site.register(Order)
admin.site.register(OrderItems)

