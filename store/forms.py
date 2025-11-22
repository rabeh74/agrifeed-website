from django import forms
from django.core.exceptions import ValidationError
from .models import Order, OrderItem, Product
import re


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'customer_phone', 'notes', 'status']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم العميل',
                'required': True
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'البريد الإلكتروني',
                'required': True
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'رقم الهاتف',
                'required': True
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'ملاحظات (اختياري)',
                'rows': 3
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def clean_customer_name(self):
        """Validate customer name"""
        name = self.cleaned_data.get('customer_name', '').strip()
        if not name:
            raise ValidationError('اسم العميل مطلوب.')
        if len(name) < 3:
            raise ValidationError('اسم العميل يجب أن يكون على الأقل 3 أحرف.')
        return name

    def clean_customer_phone(self):
        """Validate customer phone"""
        phone = self.cleaned_data.get('customer_phone', '').strip()
        if not phone:
            raise ValidationError('رقم الهاتف مطلوب.')

        # Remove spaces and dashes
        phone_digits = re.sub(r'[\s\-\(\)]', '', phone)

        # Check if it contains only digits and possibly a leading +
        if not re.match(r'^\+?\d{10,15}$', phone_digits):
            raise ValidationError('رقم الهاتف غير صحيح. يجب أن يحتوي على 10-15 رقم.')

        return phone

    def clean_customer_email(self):
        """Validate customer email"""
        email = self.cleaned_data.get('customer_email', '').strip().lower()
        if not email:
            raise ValidationError('البريد الإلكتروني مطلوب.')
        return email


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم المنتج',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'وصف المنتج',
                'rows': 4,
                'required': True
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'السعر بالجنيه المصري',
                'step': '0.01',
                'min': '0.01',
                'required': True
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'الكمية المتوفرة',
                'min': '0',
                'required': True
            })
        }

    def clean_name(self):
        """Validate product name"""
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise ValidationError('اسم المنتج مطلوب.')
        if len(name) < 3:
            raise ValidationError('اسم المنتج يجب أن يكون على الأقل 3 أحرف.')
        return name

    def clean_price(self):
        """Validate price"""
        price = self.cleaned_data.get('price')
        if price is None:
            raise ValidationError('السعر مطلوب.')
        if price <= 0:
            raise ValidationError('السعر يجب أن يكون أكبر من صفر.')
        return price

    def clean_stock(self):
        """Validate stock"""
        stock = self.cleaned_data.get('stock')
        if stock is None:
            raise ValidationError('الكمية مطلوبة.')
        if stock < 0:
            raise ValidationError('الكمية لا يمكن أن تكون سالبة.')
        return stock
