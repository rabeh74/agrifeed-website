import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agreefeed.settings')
django.setup()

from store.models import Product, Order, OrderItem
from decimal import Decimal

# Clear existing data (optional)
print("Clearing existing data...")
OrderItem.objects.all().delete()
Order.objects.all().delete()
Product.objects.all().delete()

# Create sample products
print("Creating sample products...")
products = [
    Product(
        name='هاتف ذكي سامسونج',
        description='هاتف ذكي حديث بمواصفات عالية وكاميرا ممتازة',
        price=Decimal('2500.00'),
        stock=15
    ),
    Product(
        name='لابتوب ديل',
        description='لابتوب قوي للعمل والألعاب مع معالج سريع',
        price=Decimal('4500.00'),
        stock=8
    ),
    Product(
        name='سماعات بلوتوث',
        description='سماعات لاسلكية عالية الجودة مع إلغاء الضوضاء',
        price=Decimal('350.00'),
        stock=25
    ),
    Product(
        name='ساعة ذكية',
        description='ساعة ذكية لتتبع اللياقة البدنية والصحة',
        price=Decimal('800.00'),
        stock=12
    ),
    Product(
        name='كاميرا رقمية',
        description='كاميرا احترافية لالتقاط صور عالية الدقة',
        price=Decimal('3200.00'),
        stock=5
    ),
    Product(
        name='تابلت آبل آيباد',
        description='تابلت قوي ومتعدد الاستخدامات للعمل والترفيه',
        price=Decimal('2800.00'),
        stock=10
    ),
]

for product in products:
    product.save()
    print(f"Created: {product.name}")

# Create sample orders
print("\nCreating sample orders...")

# Order 1
order1 = Order.objects.create(
    customer_name='أحمد محمد',
    customer_email='ahmed@example.com',
    customer_phone='0501234567',
    status='completed',
    notes='توصيل سريع من فضلك'
)
OrderItem.objects.create(
    order=order1,
    product=products[0],  # Samsung phone
    quantity=2,
    price=products[0].price
)
OrderItem.objects.create(
    order=order1,
    product=products[2],  # Bluetooth headphones
    quantity=1,
    price=products[2].price
)
print(f"Created Order #{order1.id} - Total: {order1.get_total_price()} ر.س")

# Order 2
order2 = Order.objects.create(
    customer_name='فاطمة علي',
    customer_email='fatima@example.com',
    customer_phone='0559876543',
    status='processing'
)
OrderItem.objects.create(
    order=order2,
    product=products[1],  # Dell laptop
    quantity=1,
    price=products[1].price
)
OrderItem.objects.create(
    order=order2,
    product=products[3],  # Smart watch
    quantity=1,
    price=products[3].price
)
print(f"Created Order #{order2.id} - Total: {order2.get_total_price()} ر.س")

# Order 3
order3 = Order.objects.create(
    customer_name='خالد السعيد',
    customer_email='khaled@example.com',
    customer_phone='0543216789',
    status='pending'
)
OrderItem.objects.create(
    order=order3,
    product=products[4],  # Digital camera
    quantity=1,
    price=products[4].price
)
OrderItem.objects.create(
    order=order3,
    product=products[5],  # iPad tablet
    quantity=1,
    price=products[5].price
)
print(f"Created Order #{order3.id} - Total: {order3.get_total_price()} ر.س")

# Order 4
order4 = Order.objects.create(
    customer_name='مريم حسن',
    customer_email='mariam@example.com',
    customer_phone='0507654321',
    status='completed'
)
OrderItem.objects.create(
    order=order4,
    product=products[2],  # Bluetooth headphones
    quantity=3,
    price=products[2].price
)
print(f"Created Order #{order4.id} - Total: {order4.get_total_price()} ر.س")

print("\n✓ Sample data added successfully!")
print(f"Total Products: {Product.objects.count()}")
print(f"Total Orders: {Order.objects.count()}")
print(f"Total Order Items: {OrderItem.objects.count()}")
