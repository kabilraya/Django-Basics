from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name = "home"),
    path("place_order/",views.place_order, name = "place_order"),
    path("order_history/",views.order_history,name = "order_history")
]