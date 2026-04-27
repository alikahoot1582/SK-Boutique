from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from .models import StitchingOrder
from products.models import Product


@login_required
def stitching_list(request):
    orders = StitchingOrder.objects.all().order_by('-created_at')
    pending = orders.filter(status='pending').count()
    in_progress = orders.filter(status='in_progress').count()
    completed = orders.filter(status='completed').count()
    delivered = orders.filter(status='delivered').count()
    return render(request, 'stitching/stitching_list.html', {
        'orders': orders,
        'pending': pending,
        'in_progress': in_progress,
        'completed': completed,
        'delivered': delivered,
    })


@login_required
def stitching_add(request):
    products = Product.objects.filter(is_active=True)
    if request.method == 'POST':
        fabric_id = request.POST.get('fabric') or None
        fabric_qty = Decimal(str(request.POST.get('fabric_quantity') or 0))

        # Deduct fabric stock if selected
        if fabric_id:
            fabric = Product.objects.get(pk=fabric_id)
            if fabric.stock < fabric_qty:
                messages.error(request, f'Insufficient fabric stock. Available: {fabric.stock}')
                return render(request, 'stitching/stitching_add.html', {'products': products})
            fabric.stock -= fabric_qty
            fabric.save()

        StitchingOrder.objects.create(
            customer_name=request.POST.get('customer_name'),
            customer_phone=request.POST.get('customer_phone') or None,
            fabric_id=fabric_id,
            fabric_quantity=fabric_qty,
            stitching_cost=Decimal(str(request.POST.get('stitching_cost') or 0)),
            delivery_date=request.POST.get('delivery_date') or None,
            status=request.POST.get('status'),
            measurements=request.POST.get('measurements') or None,
            notes=request.POST.get('notes') or None,
        )
        messages.success(request, 'Stitching order added successfully.')
        return redirect('stitching_list')

    return render(request, 'stitching/stitching_add.html', {'products': products})


@login_required
def stitching_edit(request, pk):
    order = get_object_or_404(StitchingOrder, pk=pk)
    products = Product.objects.filter(is_active=True)
    if request.method == 'POST':
        order.customer_name = request.POST.get('customer_name')
        order.customer_phone = request.POST.get('customer_phone') or None
        order.delivery_date = request.POST.get('delivery_date') or None
        order.status = request.POST.get('status')
        order.stitching_cost = Decimal(str(request.POST.get('stitching_cost') or 0))
        order.measurements = request.POST.get('measurements') or None
        order.notes = request.POST.get('notes') or None
        order.save()
        messages.success(request, 'Stitching order updated successfully.')
        return redirect('stitching_list')
    return render(request, 'stitching/stitching_edit.html', {
        'order': order,
        'products': products,
    })


@login_required
def stitching_delete(request, pk):
    order = get_object_or_404(StitchingOrder, pk=pk)
    # Return fabric stock
    if order.fabric and order.fabric_quantity:
        order.fabric.stock += order.fabric_quantity
        order.fabric.save()
    order.delete()
    messages.success(request, 'Stitching order deleted successfully.')
    return redirect('stitching_list')