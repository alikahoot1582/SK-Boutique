from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Supplier


@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by('-created_at')
    return render(request, 'suppliers/supplier_list.html', {'suppliers': suppliers})


@login_required
def supplier_add(request):
    if request.method == 'POST':
        Supplier.objects.create(
            name=request.POST.get('name'),
            business_name=request.POST.get('business_name') or None,
            phone=request.POST.get('phone') or None,
            email=request.POST.get('email') or None,
            address=request.POST.get('address') or None,
        )
        messages.success(request, 'Supplier added successfully.')
        return redirect('supplier_list')
    return render(request, 'suppliers/supplier_add.html')


@login_required
def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.name = request.POST.get('name')
        supplier.business_name = request.POST.get('business_name') or None
        supplier.phone = request.POST.get('phone') or None
        supplier.email = request.POST.get('email') or None
        supplier.address = request.POST.get('address') or None
        supplier.is_active = request.POST.get('is_active') == 'on'
        supplier.save()
        messages.success(request, 'Supplier updated successfully.')
        return redirect('supplier_list')
    return render(request, 'suppliers/supplier_edit.html', {'supplier': supplier})


@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    messages.success(request, 'Supplier deleted successfully.')
    return redirect('supplier_list')
