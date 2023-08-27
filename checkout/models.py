import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from products.models import Product

# uuid will be used to generate order number


class Order(models.Model):
    """
    These are the attribute of the whole order itself
    Postcode and County aren't neccessary in every country, so they can be empty
    auto_now_add, sets date and time to now
    Order number is unique and unchangeable, so orders can be easily found
    """
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    # The initial underscore means this function can only be used within this class
    def _generate_order_number(self):
        # This will generate a random string of 32 characters as order number
        return uuid.uuid4().hex.upper()

    # Here we are using aggregate and sum to find the total of the line items
    # We are also adding a new field to the query set called lineitem_total__sum
    def update_total(self):
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        # Here we are calculating the delivery cost.
        # Standard delivery is for number of items under the threshold amount
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
        # And this is when the threshold is reached, free delivery!
            self.delivery_cost = 0
        # From this we get the grand total and save
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    # This function overrides the original save method
    # It is checking that there is an order number, and if not, it runs the function
    # Then it saves the same way it normally would
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    # This returns the order number in string format
    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """
    These are the attributes of individual order items
    They have a relation to the order so that needs to be here
    We can access this through order.lineitems, due to the related name field
    The product is a foreign key so we can access the product model too
    The sizes can be null due to some items not being clothes
    line item total cannot be changed by user, but updates automatically
    """

    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True) # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    # The line item total needs to be timesed by the quantity correctly
    def save(self, *args, **kwargs):
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    # This returns the SKU and order number in string format
    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
