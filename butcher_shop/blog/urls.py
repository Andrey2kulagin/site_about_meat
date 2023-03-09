from django.urls import path
from .views import blog_list, blog_detail, receipt_list

urlpatterns = [
    path('', blog_list),
    path('receipts', receipt_list),
    path('receipts/<int:id>', blog_detail),
    path('<int:id>', blog_detail)
]
