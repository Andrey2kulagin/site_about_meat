from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path("blog/", include("blog.urls")),
                  path("", include("butcher_shop_app.urls"))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
