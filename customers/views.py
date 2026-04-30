from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer


@login_required
def customer_list(request):
    search = request.GET.get('search', '')
    customers = Customer.objects.all().order_by('-created_at')
    if search:
        customers = customers.filter(name__icontains=search) | customers.filter(phone__icontains=search)
    return render(request, 'customers/customer_list.html', {'customers': customers, 'search': search})


@login_required
def customer_add(request):
    if request.method == 'POST':
        Customer.objects.create(
            name=request.POST.get('name'),
            phone=request.POST.get('phone') or None,
            email=request.POST.get('email') or None,
            address=request.POST.get('address') or None,
        )
        messages.success(request, 'Customer added successfully.')
        return redirect('customer_list')
    return render(request, 'customers/customer_add.html')


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.phone = request.POST.get('phone') or None
        customer.email = request.POST.get('email') or None
        customer.address = request.POST.get('address') or None
        customer.save()
        messages.success(request, 'Customer updated successfully.')
        return redirect('customer_list')
    return render(request, 'customers/customer_edit.html', {'customer': customer})


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    messages.success(request, 'Customer deleted successfully.')
    return redirect('customer_list')