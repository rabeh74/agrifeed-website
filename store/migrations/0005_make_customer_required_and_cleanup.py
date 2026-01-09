# Migration to make customer field required and remove old customer fields

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_migrate_orders_to_customers'),
    ]

    operations = [
        # Make customer field required (not null)
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='orders',
                to='store.customer',
                verbose_name='العميل'
            ),
        ),
        # Remove old customer fields
        migrations.RemoveField(
            model_name='order',
            name='customer_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='customer_email',
        ),
        migrations.RemoveField(
            model_name='order',
            name='customer_phone',
        ),
    ]

