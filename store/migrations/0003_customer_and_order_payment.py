# Generated migration for Customer model and Order payment tracking

from django.db import migrations, models
import django.db.models.deletion
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_productentry'),
    ]

    operations = [
        # Create Customer model
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, unique=True, verbose_name='الاسم الكامل')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='رقم الهاتف')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإضافة')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')),
            ],
            options={
                'verbose_name': 'عميل',
                'verbose_name_plural': 'العملاء',
                'ordering': ['full_name'],
            },
        ),
        # Make old customer fields nullable
        migrations.AlterField(
            model_name='order',
            name='customer_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='اسم العميل (قديم)'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='رقم الهاتف (قديم)'),
        ),
        # Add paid_amount field to Order
        migrations.AddField(
            model_name='order',
            name='paid_amount',
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal('0.00'),
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(Decimal('0.00'))],
                verbose_name='المبلغ المدفوع'
            ),
        ),
        # Add customer ForeignKey to Order (nullable initially for existing orders)
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='orders',
                to='store.customer',
                verbose_name='العميل',
                null=True,  # Temporarily null for migration
                blank=True
            ),
        ),
    ]

