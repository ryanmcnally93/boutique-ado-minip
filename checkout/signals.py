from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem

# We have created this file to call the function in Order
# That calculates the totals of items and updates the fields in the admin page


# This handles signals from the post_save event
# Sender is Order Line Item
# Instance of the model that sent it, Order?
# A boolean sent by django referring to whether this is a new instance or updated one
# And kwargs "Key Word Arguements"

# This is the event listener if you like, listening to saves on the Order Line Item model
@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    # This uses the update total function on the order
    instance.order.update_total()

# This calls the same update function when an item is deleted
@receiver(post_delete, sender=OrderLineItem)
# The created parameter is not sent by the "deleted" signal, no need to mention it
def update_on_save(sender, instance, **kwargs):
    instance.order.update_total()