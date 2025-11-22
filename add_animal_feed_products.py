import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agreefeed.settings')
django.setup()

from store.models import Product, Order, OrderItem
from decimal import Decimal

# Clear existing data
print("Clearing existing data...")
OrderItem.objects.all().delete()
Order.objects.all().delete()
Product.objects.all().delete()

# Create animal feed products
print("\n" + "="*60)
print("Creating Animal Feed Products...")
print("="*60)

products_data = [
    {
        'name': 'علف أبقار عالي البروتين',
        'description': 'علف متكامل للأبقار الحلوب يحتوي على نسبة عالية من البروتين والفيتامينات لزيادة إنتاج الحليب. مصنع من أجود أنواع الحبوب والبقوليات.',
        'price': Decimal('450.00'),
        'stock': 50
    },
    {
        'name': 'علف أغنام وماعز',
        'description': 'خلطة علفية متوازنة للأغنام والماعز تساعد على النمو السريع وزيادة الوزن. غني بالطاقة والمعادن الضرورية.',
        'price': Decimal('380.00'),
        'stock': 75
    },
    {
        'name': 'علف دواجن تسمين',
        'description': 'علف تسمين للدواجن (دجاج لحم) يساعد على النمو السريع وتحسين معدل التحويل الغذائي. خالي من الهرمونات.',
        'price': Decimal('320.00'),
        'stock': 100
    },
    {
        'name': 'علف دجاج بياض',
        'description': 'علف مخصص للدجاج البياض لزيادة إنتاج البيض. يحتوي على نسبة عالية من الكالسيوم والبروتين.',
        'price': Decimal('340.00'),
        'stock': 90
    },
    {
        'name': 'علف خيول ومهور',
        'description': 'علف متكامل للخيول والمهور يحتوي على الشعير والشوفان والفيتامينات. يعطي الطاقة والنشاط.',
        'price': Decimal('550.00'),
        'stock': 30
    },
    {
        'name': 'علف أرانب',
        'description': 'علف مخصص للأرانب بجميع أعمارها. غني بالألياف والبروتينات النباتية اللازمة للنمو السليم.',
        'price': Decimal('280.00'),
        'stock': 60
    },
    {
        'name': 'علف جمال (إبل)',
        'description': 'خلطة علفية متكاملة للإبل تحتوي على الحبوب والأملاح المعدنية. مناسب للجمال في جميع الظروف المناخية.',
        'price': Decimal('420.00'),
        'stock': 40
    },
    {
        'name': 'علف عجول رضيعة',
        'description': 'علف بادئ للعجول الرضيعة من عمر أسبوعين. سهل الهضم ويساعد على النمو الصحي السريع.',
        'price': Decimal('480.00'),
        'stock': 35
    },
    {
        'name': 'علف مركز للماشية',
        'description': 'علف مركز عالي القيمة الغذائية للماشية بجميع أنواعها. يخلط مع الأعلاف الخشنة للحصول على أفضل النتائج.',
        'price': Decimal('520.00'),
        'stock': 45
    },
    {
        'name': 'علف بط وإوز',
        'description': 'علف مخصص للبط والإوز يساعد على النمو وزيادة الوزن. مقاوم للماء ومناسب لطريقة تغذيتهم.',
        'price': Decimal('310.00'),
        'stock': 55
    },
    {
        'name': 'علف حمام',
        'description': 'خلطة من الحبوب المختارة للحمام. تحتوي على الذرة والقمح والعدس والبازلاء لتغذية متكاملة.',
        'price': Decimal('220.00'),
        'stock': 80
    },
    {
        'name': 'علف أسماك (زريعة)',
        'description': 'علف طافي للأسماك الصغيرة (الزريعة). غني بالبروتين الحيواني والنباتي لنمو سريع وصحي.',
        'price': Decimal('360.00'),
        'stock': 70
    },
]

print("\nAdding products to database...")
for product_data in products_data:
    product = Product.objects.create(**product_data)
    print(f"✓ {product.name} - {product.price} ج.م (المخزون: {product.stock})")

print("\n" + "="*60)
print(f"✅ Successfully added {Product.objects.count()} animal feed products!")
print("="*60)

print("\n📋 Product Summary:")
print(f"   Total Products: {Product.objects.count()}")
print(f"   Total Stock Value: {sum(p.price * p.stock for p in Product.objects.all())} ج.م")
print(f"   Average Price: {Product.objects.all().aggregate(avg_price=django.db.models.Avg('price'))['avg_price']:.2f} ج.م")

print("\n💡 Note: You can add product images through the web interface.")
print("   Go to: http://127.0.0.1:8000/ and click 'تعديل' on any product.")
