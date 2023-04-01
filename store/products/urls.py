from django.urls import include, path
from django.views.decorators.cache import cache_page

from products.views import BasketDeleteView, ProductsListView, basket_add

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    # path('', cache_page(30)(ProductsListView.as_view()), name='index'),
    path('category/<int:category_id>/', ProductsListView.as_view(), name='category'),
    path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),
    # path('category/<int:category_id>/page/<int:page_number>', products_by_cat, name='category_paginator'),
    # path('page/<int:page_number>/', products, name='paginator'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),  # ../products/baskets/add/<product_id>/
    path('baskets/remove/<int:basket_id>/', BasketDeleteView.as_view(), name='basket_remove'),
    # path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
