from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Customer(models.Model):
    full_name = models.CharField(max_length=200, unique=True, verbose_name='الاسم الكامل')
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='رقم الهاتف')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإضافة')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'عميل'
        verbose_name_plural = 'العملاء'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name

    def get_total_debt(self):
        """Calculate total remaining money across all orders"""
        return sum(order.get_remaining_amount() for order in self.orders.all())


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='اسم المنتج')
    description = models.TextField(verbose_name='الوصف')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='صورة المنتج')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='السعر'
    )
    stock = models.PositiveIntegerField(default=0, verbose_name='الكمية المتوفرة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإضافة')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'منتج'
        verbose_name_plural = 'المنتجات'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def has_stock(self, quantity):
        """Check if product has sufficient stock"""
        return self.stock >= quantity

    def decrease_stock(self, quantity):
        """Decrease stock by quantity. Raises ValueError if insufficient stock."""
        if not self.has_stock(quantity):
            raise ValueError(f'الكمية المطلوبة ({quantity}) غير متوفرة. المتوفر: {self.stock}')
        self.stock -= quantity
        self.save(update_fields=['stock'])

    def increase_stock(self, quantity):
        """Increase stock by quantity (for cancelled orders)"""
        self.stock += quantity
        self.save(update_fields=['stock'])


class Order(models.Model):
    STATUS_CHOICES = [
        ('completed', 'مكتمل'),
        ('cancelled', 'ملغي'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='العميل'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='completed',
        verbose_name='الحالة'
    )
    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='المبلغ المدفوع'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الطلب')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')
    notes = models.TextField(blank=True, verbose_name='ملاحظات')

    class Meta:
        verbose_name = 'طلب'
        verbose_name_plural = 'الطلبات'
        ordering = ['-created_at']

    def __str__(self):
        return f'طلب #{self.id} - {self.customer.full_name}'

    def get_total_price(self):
        """Calculate total order price from items"""
        return sum(item.get_total_price() for item in self.items.all())

    def get_remaining_amount(self):
        """Calculate remaining unpaid amount"""
        total = self.get_total_price()
        return max(total - self.paid_amount, Decimal('0.00'))

    def is_fully_paid(self):
        """Check if order is fully paid"""
        return self.get_remaining_amount() == Decimal('0.00')


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name='الطلب'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='المنتج'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='الكمية'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='السعر'
    )

    class Meta:
        verbose_name = 'عنصر طلب'
        verbose_name_plural = 'عناصر الطلبات'

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def get_total_price(self):
        return self.quantity * self.price
