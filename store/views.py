from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Product, Order, OrderItem
from .forms import OrderForm, ProductForm


@login_required
def dashboard(request):
    """Dashboard with order statistics and date filtering"""
    # Get filter parameters
    filter_type = request.GET.get('filter', 'all')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Start with all orders
    orders = Order.objects.all()

    # Apply date filtering
    today = datetime.now().date()
    filter_label = 'جميع الطلبات'

    if filter_type == 'today':
        orders = orders.filter(created_at__date=today)
        filter_label = 'اليوم'
    elif filter_type == 'week':
        week_start = today - timedelta(days=today.weekday())
        orders = orders.filter(created_at__date__gte=week_start)
        filter_label = 'هذا الأسبوع'
    elif filter_type == 'month':
        month_start = today.replace(day=1)
        orders = orders.filter(created_at__date__gte=month_start)
        filter_label = 'هذا الشهر'
    elif filter_type == 'custom' and start_date and end_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            orders = orders.filter(created_at__date__gte=start, created_at__date__lte=end)
            filter_label = f'من {start_date} إلى {end_date}'
        except ValueError:
            messages.error(request, 'تاريخ غير صحيح')

    # Calculate statistics
    total_orders = orders.count()

    # Calculate total revenue
    total_revenue = Decimal('0.00')
    for order in orders:
        total_revenue += order.get_total_price()

    # Calculate average order value
    average_order = total_revenue / total_orders if total_orders > 0 else Decimal('0.00')

    # Get orders with their totals for display
    orders_with_totals = []
    for order in orders.order_by('-created_at'):
        orders_with_totals.append({
            'order': order,
            'total': order.get_total_price()
        })

    # Status breakdown
    status_stats = {
        'completed': orders.filter(status='completed').count(),
        'cancelled': orders.filter(status='cancelled').count(),
    }

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'average_order': average_order,
        'orders_with_totals': orders_with_totals,
        'filter_type': filter_type,
        'filter_label': filter_label,
        'start_date': start_date,
        'end_date': end_date,
        'status_stats': status_stats,
    }

    return render(request, 'store/dashboard.html', context)


@login_required
def product_list(request):
    """Product list with search and filter"""
    products = Product.objects.all()

    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Stock filter
    stock_filter = request.GET.get('stock', 'all')
    if stock_filter == 'in_stock':
        products = products.filter(stock__gt=0)
    elif stock_filter == 'out_of_stock':
        products = products.filter(stock=0)
    elif stock_filter == 'low_stock':
        products = products.filter(stock__gt=0, stock__lte=10)

    # Sort
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = ['-created_at', 'created_at', 'name', '-name', 'price', '-price', 'stock', '-stock']
    if sort_by in valid_sorts:
        products = products.order_by(sort_by)

    context = {
        'products': products,
        'search_query': search_query,
        'stock_filter': stock_filter,
        'sort_by': sort_by,
    }
    return render(request, 'store/product_list.html', context)


@login_required
def order_list(request):
    """Order list with search and filter"""
    orders = Order.objects.all()

    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        orders = orders.filter(customer_name__icontains=search_query) | orders.filter(customer_phone__icontains=search_query)

    # Status filter
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        orders = orders.filter(status=status_filter)

    # Date filter
    date_filter = request.GET.get('date', 'all')
    if date_filter == 'today':
        from datetime import datetime
        today = datetime.now().date()
        orders = orders.filter(created_at__date=today)
    elif date_filter == 'week':
        from datetime import datetime, timedelta
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        orders = orders.filter(created_at__date__gte=week_start)
    elif date_filter == 'month':
        from datetime import datetime
        today = datetime.now().date()
        month_start = today.replace(day=1)
        orders = orders.filter(created_at__date__gte=month_start)

    # Sort
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = ['-created_at', 'created_at', 'customer_name', '-customer_name']
    if sort_by in valid_sorts:
        orders = orders.order_by(sort_by)

    context = {
        'orders': orders,
        'search_query': search_query,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'sort_by': sort_by,
    }
    return render(request, 'store/order_list.html', context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()
    total_price = order.get_total_price()
    context = {
        'order': order,
        'order_items': order_items,
        'total_price': total_price
    }
    return render(request, 'store/order_detail.html', context)


@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)

        # Get product quantities from POST data
        product_ids = request.POST.getlist('product_id[]')
        quantities = request.POST.getlist('quantity[]')

        # Validate form first
        if not form.is_valid():
            # Don't show generic message - field-specific errors will show
            products = Product.objects.filter(stock__gt=0)
            return render(request, 'store/create_order.html', {'form': form, 'products': products})

        # Validate that we have products
        if not product_ids or not quantities:
            messages.error(request, 'يرجى إضافة منتج واحد على الأقل إلى الطلب.')
            products = Product.objects.filter(stock__gt=0)
            return render(request, 'store/create_order.html', {'form': form, 'products': products})

        # Prepare order items data and validate
        order_items_data = []
        seen_products = set()

        for product_id, quantity_str in zip(product_ids, quantities):
            # Skip empty entries
            if not product_id or not quantity_str:
                continue

            try:
                product_id = int(product_id)
                quantity = int(quantity_str)
            except (ValueError, TypeError):
                messages.error(request, 'بيانات غير صحيحة في المنتجات.')
                products = Product.objects.filter(stock__gt=0)
                return render(request, 'store/create_order.html', {'form': form, 'products': products})

            # Validate quantity is positive
            if quantity <= 0:
                messages.error(request, 'الكمية يجب أن تكون أكبر من صفر.')
                products = Product.objects.filter(stock__gt=0)
                return render(request, 'store/create_order.html', {'form': form, 'products': products})

            # Check for duplicate products
            if product_id in seen_products:
                messages.error(request, f'تم إضافة نفس المنتج أكثر من مرة. يرجى دمج الكميات.')
                products = Product.objects.filter(stock__gt=0)
                return render(request, 'store/create_order.html', {'form': form, 'products': products})

            seen_products.add(product_id)
            order_items_data.append({
                'product_id': product_id,
                'quantity': quantity
            })

        # Must have at least one valid product
        if not order_items_data:
            messages.error(request, 'يرجى إضافة منتج واحد على الأقل إلى الطلب.')
            products = Product.objects.filter(stock__gt=0)
            return render(request, 'store/create_order.html', {'form': form, 'products': products})

        # Use atomic transaction to ensure data consistency
        try:
            with transaction.atomic():
                # Create the order
                order = form.save()

                # Process each product with stock locking
                for item_data in order_items_data:
                    product_id = item_data['product_id']
                    quantity = item_data['quantity']

                    # Lock the product row for update to prevent race conditions
                    try:
                        product = Product.objects.select_for_update().get(id=product_id)
                    except Product.DoesNotExist:
                        # Rollback will happen automatically
                        raise ValidationError(f'المنتج برقم {product_id} غير موجود.')

                    # Check stock availability
                    if not product.has_stock(quantity):
                        # Rollback will happen automatically
                        raise ValidationError(
                            f'الكمية المطلوبة من "{product.name}" غير متوفرة. '
                            f'المطلوب: {quantity}، المتوفر: {product.stock}'
                        )

                    # Create order item
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price
                    )

                    # Decrease stock
                    product.decrease_stock(quantity)

                # If we reach here, everything is successful
                messages.success(request, f'تم إنشاء الطلب #{order.id} بنجاح!')
                return redirect('store:order_detail', order_id=order.id)

        except ValidationError as e:
            # Validation errors (stock issues, product not found, etc.)
            messages.error(request, str(e))
        except ValueError as e:
            # Stock validation errors from model
            messages.error(request, str(e))
        except Exception as e:
            # Unexpected errors
            messages.error(request, f'حدث خطأ أثناء إنشاء الطلب: {str(e)}')

        # If we reach here, there was an error
        products = Product.objects.filter(stock__gt=0)
        return render(request, 'store/create_order.html', {'form': form, 'products': products})

    else:
        # GET request - show form
        form = OrderForm()

    products = Product.objects.filter(stock__gt=0)
    context = {
        'form': form,
        'products': products
    }
    return render(request, 'store/create_order.html', context)


# ================== PRODUCT MANAGEMENT ==================

@login_required
def add_product(request):
    """Add new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'تم إضافة المنتج "{product.name}" بنجاح!')
            return redirect('store:product_list')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء في النموذج.')
    else:
        form = ProductForm()

    return render(request, 'store/product_form.html', {'form': form, 'action': 'add'})


@login_required
def edit_product(request, product_id):
    """Edit existing product"""
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'تم تحديث المنتج "{product.name}" بنجاح!')
            return redirect('store:product_list')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء في النموذج.')
    else:
        form = ProductForm(instance=product)

    return render(request, 'store/product_form.html', {
        'form': form,
        'action': 'edit',
        'product': product
    })


@login_required
def delete_product(request, product_id):
    """Delete product"""
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'تم حذف المنتج "{product_name}" بنجاح!')
        return redirect('store:product_list')

    return render(request, 'store/product_confirm_delete.html', {'product': product})


# ================== ORDER MANAGEMENT ==================

@login_required
def edit_order(request, order_id):
    """Edit existing order (only customer info and status)"""
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            messages.success(request, f'تم تحديث الطلب #{order.id} بنجاح!')
            return redirect('order_detail', order_id=order.id)
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء في النموذج.')
    else:
        form = OrderForm(instance=order)

    return render(request, 'store/order_form.html', {
        'form': form,
        'order': order
    })


@login_required
def delete_order(request, order_id):
    """Delete order and restore stock"""
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # Restore stock for all items
        with transaction.atomic():
            for item in order.items.all():
                product = item.product
                product.increase_stock(item.quantity)

            order_number = order.id
            order.delete()

        messages.success(request, f'تم حذف الطلب #{order_number} وإعادة المخزون بنجاح!')
        return redirect('store:order_list')

    total_price = order.get_total_price()
    return render(request, 'store/order_confirm_delete.html', {
        'order': order,
        'total_price': total_price
    })
