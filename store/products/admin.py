from django.contrib import admin

from products.models import Basket, Product, ProductCategory

# admin.site.register(Product)
admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'description', ('price', 'quantity'), 'stripe_product_price_id', 'category', 'image')
    readonly_fields = ('description',)
    search_fields = ('name',)
    ordering = ('-name',)


class BasketAdmin(admin.TabularInline):  # TabularInline можно применять если есть FK связь
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0