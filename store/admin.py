from django.contrib import admin
from .models import Product, Order, OrderItem, Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'get_total_debt', 'created_at']
    list_filter = ['created_at']
    search_fields = ['full_name', 'phone_number']
    
    def get_total_debt(self, obj):
        return f'{obj.get_total_debt()} ج.م'
    get_total_debt.short_description = 'إجمالي الديون'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_customer_name', 'status', 'get_total', 'paid_amount', 'get_remaining', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer__full_name', 'customer__phone_number', 'customer_name']
    list_editable = ['status']
    inlines = [OrderItemInline]
    raw_id_fields = ['customer']

    def get_customer_name(self, obj):
        return obj.customer.full_name if obj.customer else obj.customer_name
    get_customer_name.short_description = 'العميل'

    def get_total(self, obj):
        return f'{obj.get_total_price()} ج.م'
    get_total.short_description = 'الإجمالي'

    def get_remaining(self, obj):
        return f'{obj.get_remaining_amount()} ج.م'
    get_remaining.short_description = 'المتبقي'
