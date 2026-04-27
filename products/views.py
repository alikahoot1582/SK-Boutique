from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, SubCategory, Manufacturer, Product


# ─── Categories ───────────────────────────────────────
@login_required
def category_list(request):
    categories = Category.objects.all().order_by('-created_at')
    return render(request, 'products/category_list.html', {'categories': categories})


@login_required
def category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            messages.success(request, 'Category added successfully.')
            return redirect('category_list')
    return render(request, 'products/category_add.html')


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully.')
    return redirect('category_list')


# ─── Sub Categories ───────────────────────────────────
@login_required
def subcategory_list(request):
    subcategories = SubCategory.objects.all().order_by('-created_at')
    return render(request, 'products/subcategory_list.html', {'subcategories': subcategories})


@login_required
def subcategory_add(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        if name and category_id:
            SubCategory.objects.create(name=name, category_id=category_id)
            messages.success(request, 'Sub Category added successfully.')
            return redirect('subcategory_list')
    return render(request, 'products/subcategory_add.html', {'categories': categories})


@login_required
def subcategory_delete(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)
    subcategory.delete()
    messages.success(request, 'Sub Category deleted successfully.')
    return redirect('subcategory_list')


# ─── Manufacturers ────────────────────────────────────
@login_required
def manufacturer_list(request):
    manufacturers = Manufacturer.objects.all().order_by('-created_at')
    return render(request, 'products/manufacturer_list.html', {'manufacturers': manufacturers})


@login_required
def manufacturer_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Manufacturer.objects.create(name=name)
            messages.success(request, 'Manufacturer added successfully.')
            return redirect('manufacturer_list')
    return render(request, 'products/manufacturer_add.html')


@login_required
def manufacturer_delete(request, pk):
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    manufacturer.delete()
    messages.success(request, 'Manufacturer deleted successfully.')
    return redirect('manufacturer_list')


# ─── Products ─────────────────────────────────────────
@login_required
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/product_list.html', {'products': products})


@login_required
def product_add(request):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    manufacturers = Manufacturer.objects.all()

    if request.method == 'POST':
        try:
            Product.objects.create(
                name=request.POST.get('name'),
                product_code=request.POST.get('product_code') or None,
                category_id=request.POST.get('category') or None,
                sub_category_id=request.POST.get('sub_category') or None,
                manufacturer_id=request.POST.get('manufacturer') or None,
                unit_type=request.POST.get('unit_type'),
                purchase_price=float(request.POST.get('purchase_price') or 0),
                sale_price=float(request.POST.get('sale_price') or 0),
                stock=float(request.POST.get('stock') or 0),
                stock_alert=float(request.POST.get('stock_alert') or 5),
            )
            messages.success(request, 'Product added successfully.')
            return redirect('product_list')
        except Exception as e:
            messages.error(request, f'Error adding product: {str(e)}')

    return render(request, 'products/product_add.html', {
        'categories': categories,
        'subcategories': subcategories,
        'manufacturers': manufacturers,
    })


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    manufacturers = Manufacturer.objects.all()

    if request.method == 'POST':
        try:
            product.name = request.POST.get('name')
            product.product_code = request.POST.get('product_code') or None
            product.category_id = request.POST.get('category') or None
            product.sub_category_id = request.POST.get('sub_category') or None
            product.manufacturer_id = request.POST.get('manufacturer') or None
            product.unit_type = request.POST.get('unit_type')
            product.purchase_price = float(request.POST.get('purchase_price') or 0)
            product.sale_price = float(request.POST.get('sale_price') or 0)
            product.stock = float(request.POST.get('stock') or 0)
            product.stock_alert = float(request.POST.get('stock_alert') or 5)
            product.is_active = request.POST.get('is_active') == 'on'
            product.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_list')
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')

    return render(request, 'products/product_edit.html', {
        'product': product,
        'categories': categories,
        'subcategories': subcategories,
        'manufacturers': manufacturers,
    })


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('product_list')