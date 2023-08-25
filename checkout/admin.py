from django.contrib import admin
from .models import Order, OrderLineItem

# This document adds fields to the admin page


# Allows us to make changes to individual line items in the admin interface
class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    # These will be calculated by the model, not changed by admin
    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total',)

    # Writing all the fields here isn't required
    # But means we can structure the order of the attributes
    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total',)

    # This restricts the columns that show up to only a few key items
    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    # Order items by date, most recent at the top
    ordering = ('-date',)

# We don't need to register the line items as they are in the Order class
admin.site.register(Order, OrderAdmin)