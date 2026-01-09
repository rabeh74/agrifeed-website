# Data migration to convert existing orders to use Customer model

from django.db import migrations
from django.db.models import Q


def migrate_orders_to_customers(apps, schema_editor):
    """
    Migrate existing orders to use Customer model:
    1. Create Customer objects from unique customer names
    2. Link orders to these customers
    """
    Order = apps.get_model('store', 'Order')
    Customer = apps.get_model('store', 'Customer')
    
    # Get all orders
    orders = Order.objects.all()
    
    if not orders.exists():
        print("No orders found to migrate.")
        return
    
    print(f"Found {orders.count()} orders to migrate...")
    
    # Dictionary to track created customers {name: customer_object}
    customer_cache = {}
    
    # Counter for statistics
    customers_created = 0
    orders_migrated = 0
    orders_skipped = 0
    
    for order in orders:
        # Skip if order already has a customer assigned
        if order.customer_id:
            orders_skipped += 1
            continue
            
        # Get customer name from old field
        customer_name = order.customer_name
        
        if not customer_name or not customer_name.strip():
            print(f"  ⚠️  Order #{order.id} has no customer name, skipping...")
            orders_skipped += 1
            continue
        
        customer_name = customer_name.strip()
        
        # Check if we've already created this customer
        if customer_name in customer_cache:
            customer = customer_cache[customer_name]
        else:
            # Try to find existing customer with this name
            customer = Customer.objects.filter(full_name=customer_name).first()
            
            if not customer:
                # Create new customer
                # Get phone from old field (if available)
                phone = order.customer_phone if order.customer_phone else ''
                
                try:
                    customer = Customer.objects.create(
                        full_name=customer_name,
                        phone_number=phone.strip() if phone else None
                    )
                    customers_created += 1
                    print(f"  ✓ Created customer: {customer_name}")
                except Exception as e:
                    # If customer name already exists (race condition), fetch it
                    customer = Customer.objects.filter(full_name=customer_name).first()
                    if not customer:
                        print(f"  ✗ Error creating customer '{customer_name}': {e}")
                        orders_skipped += 1
                        continue
            
            # Cache the customer
            customer_cache[customer_name] = customer
        
        # Link order to customer
        order.customer = customer
        order.save(update_fields=['customer'])
        orders_migrated += 1
    
    print(f"\n✅ Migration completed:")
    print(f"   - Customers created: {customers_created}")
    print(f"   - Orders migrated: {orders_migrated}")
    print(f"   - Orders skipped: {orders_skipped}")


def reverse_migration(apps, schema_editor):
    """
    Reverse migration: Copy customer data back to order fields
    """
    Order = apps.get_model('store', 'Order')
    
    orders = Order.objects.filter(customer__isnull=False)
    
    print(f"Reversing migration for {orders.count()} orders...")
    
    for order in orders:
        order.customer_name = order.customer.full_name
        order.customer_phone = order.customer.phone_number if order.customer.phone_number else ''
        order.customer_email = ''  # Email field will be removed
        order.save(update_fields=['customer_name', 'customer_phone', 'customer_email'])
    
    print("✅ Reverse migration completed")


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_customer_and_order_payment'),
    ]

    operations = [
        migrations.RunPython(
            migrate_orders_to_customers,
            reverse_migration
        ),
    ]

