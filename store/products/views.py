from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory
from users.models import User

# функции = контроллеры = обработчики запросов, вьюхи


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Галерея'

    # def get_context_data(self, **kwargs):
    #     context = super(IndexView, self).get_context_data()
    #     context['title'] = 'Галерея'
    #     return context


# def index(request):
#     context = {
#         'title': 'Галерея',
#         'username': 'name1',
#         'is_promotion': True,
#     }
#     return render(request, 'products/index.html', context=context)


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    paginate_by = 3
    title = 'Галерея - Каталог'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            return Product.objects.filter(category_id=category_id)
        return Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        context['cat_id'] = self.kwargs.get('category_id')
        return context

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(ProductsListView, self).get_context_data()
    #     categories = cache.get('categories')
    #     if not categories:
    #         context['categories'] = ProductCategory.objects.all()
    #         cache.set('categories', context['categories'], 30)
    #     else:
    #         context['categories'] = categories
    #     # context['title'] = 'Галерея - Каталог'
    #     # context['categories'] = ProductCategory.objects.all()
    #     return context


# def products(request, page_number=1):
#     products = Product.objects.all()
#
#     per_page = 3
#     paginator = Paginator(products, per_page)
#     products_paginator = paginator.page(page_number)
#
#     context = {
#         'title': 'Галерея - Каталог',
#         'categories': ProductCategory.objects.all(),
#         'products': products_paginator,
#         'cat_id': None,
#     }
#
#     return render(request=request, template_name='products/products.html', context=context)


# def products_by_cat(request, category_id, page_number=1):
#     products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
#
#     per_page = 3
#     paginator = Paginator(products, per_page)
#     products_paginator = paginator.page(page_number)
#     cat_id = category_id
#
#     context = {
#         'title': 'Галерея - Каталог',
#         'categories': ProductCategory.objects.all(),
#         'products': products_paginator,
#         'cat_id': cat_id,
#     }
#
#     return render(request=request, template_name='products/products.html', context=context)


# class BasketCreateView(CreateView):
#     model = Basket
#
#     def post(self, request, *args, **kwargs):
#         product = Product.objects.get(id=self.kwargs.get('product_id'))
#         baskets = Basket.objects.filter(user=request.user, product=product)
#
#         if not baskets.exists():
#             ... решили оставить функцию


@login_required
def basket_add(request, product_id):
    Basket.create_or_update(product_id, request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class BasketDeleteView(LoginRequiredMixin, DeleteView):
    model = Basket
    # success_url = reverse_lazy('users:profile')
    pk_url_kwarg = 'basket_id'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.id,))

# @login_required
# def basket_remove(request, basket_id):
#     basket = Basket.objects.get(id=basket_id)
#     basket.delete()
#     return HttpResponseRedirect(request.META['HTTP_REFERER'])
