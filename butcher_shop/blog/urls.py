from django.urls import path
from .views import blog_list, blog_detail, receipt_list

urlpatterns = [
    path('', blog_list, name="blog_list"),
    path('receipts', receipt_list, name="receipts"),
    path('receipts/<int:id>', blog_detail, name="receipts_detail"),
    path('<int:id>', blog_detail, name="blog_detail")
]
