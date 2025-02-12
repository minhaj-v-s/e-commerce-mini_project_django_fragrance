from django.urls import path
from . import views
urlpatterns = [
    path("",views.home,name="home"),
    path("product/<str:pk>/",views.product,name="product"),
    path("cart/<str:pk>/",views.cart,name='cart'),
    path("view_cart/",views.view_cart,name="view_cart"),
    path("cart_update/<str:pk>/<str:action>/",views.cart_update,name='cart_update'),
    path("cart_remove/<str:pk>/<str:action>",views.cart_remove,name="cart_remove"),
]