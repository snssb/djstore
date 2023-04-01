from django.urls import include, path

from orders.views import (CanceledTemplateView, OrderCreateView,
                          OrderDetailView, OrderListView, SuccessTemplateView)

app_name = 'orders'

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('', OrderListView.as_view(), name='orders_list'),
    path('order/<int:order_id>/', OrderDetailView.as_view(), name='order'),
    path('order-success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
]
