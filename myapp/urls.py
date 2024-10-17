from django.urls import path
from .views import register_user, upload_product

urlpatterns = [
    path('api/register/', register_user, name='register-user'),
    path('api/upload-product/', upload_product, name='upload-product'),
]