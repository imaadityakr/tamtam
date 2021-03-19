from django.urls import path
from . import views as qrcode_api

urlpatterns = [
    path('login/', qrcode_api.LoginView.as_view(), name='superuser-login'),
    path('logout/', qrcode_api.LogoutView.as_view(), name='superuser-logout'),
    path('product-detail/', qrcode_api.ListProduct.as_view(), name="product-detail"),
	]