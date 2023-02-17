from django.contrib import admin
from .models import Product, Application, UserAdditionalInfo

admin.site.register(Product)
admin.site.register(Application)
admin.site.register(UserAdditionalInfo)
