from django.db import models
from ..products.models import Product
from ..customers.models import Customer
from django.db.models.signals import pre_save, post_save, post_delete


class Invoice(models.Model):
    """Model definition for Invoice."""

    # TODO: return customer name from order

    PAYMENT_CHOICES = [
        ("cs", "cash"),
        ("ca", "card"),
        ("cu", "cupon"),
    ]
    invoice_number = models.CharField(max_length=12)
    date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    order = models.OneToOneField("Order", on_delete=models.CASCADE)
    payment = models.CharField(max_length=2, choices=PAYMENT_CHOICES)

    def __str__(self):
        return str(self.order.id)
    
    def total(self):
        return self.order.total

def invoice_post_save_receiver(sender, instance, *args, **kwargs):
    """Calls update_status def from Order Model"""
    instance.order.update_status("pa")

post_save.connect(invoice_post_save_receiver, sender=Invoice)

class Order(models.Model):
    """Customer orders and state management."""

    # TODO: delivery_type: To eat here or carry out

    STATUS_CHOICES = [
        ("re", "received"),
        ("pa", "payed"),
        ("co", "cooking"),
        ("rd", "ready"),
        ("de", "delivered"),
    ]
    date = models.DateTimeField(auto_now_add=True)
    product = models.ManyToManyField(Product, through="OrderDetail")
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default="re")
    total = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def update_total(self):
        total = 0
        products = self.orderdetail_set.all()
        for product in products:
            total += product.subtotal
        self.total = total
        self.save()

    def update_status(self, choice):
        self.status = choice
        self.save()

    def __str__(self):
        return str(self.id)


class OrderDetail(models.Model):
    """Order detail as quantity of each product and price."""

    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def remove(self):
        return self.product.remove_from_order()

    def __str__(self):
        return self.product.name


def order_product_pre_save_receiver(sender, instance, *args, **kwargs):
    """Pre saves the price and subtotal of orders."""
    qty = instance.quantity
    if qty >= 1:
        price = instance.product.price
        subtotal = qty * price
        instance.price = price
        instance.subtotal = subtotal


pre_save.connect(order_product_pre_save_receiver, sender=OrderDetail)

def order_product_post_save_receiver(sender, instance, *args, **kwargs):
    """Calls update_total def from Order Model"""
    instance.order.update_total()

post_save.connect(order_product_post_save_receiver, sender=OrderDetail)

post_delete.connect(order_product_post_save_receiver, sender=OrderDetail)