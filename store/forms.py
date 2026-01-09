from django import forms
from django.core.exceptions import ValidationError
from .models import Order, OrderItem, Product, Customer
import re


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'phone_number']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'الاسم الكامل',
                'required': True
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'رقم الهاتف (اختياري)',
                'required': False
            })
        }

    def clean_full_name(self):
        """Validate customer name"""
        name = self.cleaned_data.get('full_name', '').strip()
        if not name:
            raise ValidationError('الاسم الكامل مطلوب.')
        if len(name) < 3:
            raise ValidationError('الاسم يجب أن يكون على الأقل 3 أحرف.')
        return name

    def clean_phone_number(self):
        """Validate customer phone if provided"""
        phone = self.cleaned_data.get('phone_number', '').strip()
        
        if not phone:
            return ''

        # Remove spaces and dashes
        phone_digits = re.sub(r'[\s\-\(\)]', '', phone)

        # Check if it contains only digits and possibly a leading +
        if not re.match(r'^\+?\d{10,15}$', phone_digits):
            raise ValidationError('رقم الهاتف غير صحيح. يجب أن يحتوي على 10-15 رقم.')

        return phone


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'paid_amount', 'notes', 'status']
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'paid_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'المبلغ المدفوع',
                'step': '0.01',
                'min': '0.00',
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

    def clean_paid_amount(self):
        """Validate paid amount"""
        paid_amount = self.cleaned_data.get('paid_amount')
        if paid_amount is None:
            raise ValidationError('المبلغ المدفوع مطلوب.')
        if paid_amount < 0:
            raise ValidationError('المبلغ المدفوع لا يمكن أن يكون سالباً.')
        return paid_amount


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
