from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        # Here we are creating a form using the Order model
        # And only using fields that are not automatically filled in
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    # Here we are overriding the normal init method

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        # This is the default init method
        super().__init__(*args, **kwargs)
        # Here we have created a dictionary of form fields
        # They will show up in the form fields rather than
        # clunky field names and empty text boxes in template
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        # This is just setting the focus automatically to where we want it
        self.fields['full_name'].widget.attrs['autofocus'] = True
        # This adds stars to the required fields
        # And sets revelant placeholder names to their inputs
        # Also adds a css class
        # And removes labels as we have placeholders
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
        # This is advanced form customization!