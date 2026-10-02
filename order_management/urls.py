from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("place_order/", views.place_order, name="place_order"),
    path("order_history/", views.order_history, name="order_history"),
    path("order/<int:order_id>/", views.order_view, name="view_order"),
    path("order/<int:order_id>/update/", views.order_update, name="order_update"),
    path("order/<int:order_id>/delete/", views.order_delete, name="order_delete"),
]