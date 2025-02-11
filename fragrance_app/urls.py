from django.urls import path
from . import views
urlpatterns = [
    path("",views.home,name="home"),
    path("cart/<str:pk>",views.cart,name='cart'),
    path("product/<str:pk>",views.product,name="product")
]