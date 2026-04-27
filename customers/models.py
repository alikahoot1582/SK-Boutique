from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def total_purchases(self):
        try:
            return self.sales.count()
        except:
            return 0

    @property
    def total_spent(self):
        try:
            return sum(sale.net_total for sale in self.sales.all())
        except:
            return 0