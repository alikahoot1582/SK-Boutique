from django.db import models
from products.models import Product
from customers.models import Customer


class StitchingOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('delivered', 'Delivered'),
    ]

    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    fabric = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stitching_orders'
    )
    fabric_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stitching_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    measurements = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.customer_name}"
