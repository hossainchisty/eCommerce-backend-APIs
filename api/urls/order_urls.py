from django.urls import path
from api.views import order_views as views


urlpatterns = [
    path("", views.getOrder.as_view(), name="orders"),
    path("myorder", views.getMyOrders.as_view(), name="order"),
    path("<int:pk>", views.getOrderById, name="getOrderById"),
    path("pay/<int:pk>", views.OrderToPaid, name="OrderToPaid"),
    path("deliver/<int:pk>", views.OrderToDelivered, name="OrderToDelivered"),
    path("add", views.addOrderItem, name="addOrderItem"),
]
