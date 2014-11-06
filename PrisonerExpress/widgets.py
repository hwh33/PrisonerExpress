from django import forms
from django.forms import widgets

class AddressWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        _widgets = (
            widgets.TextInput(attrs=attrs), #Address Line 1
            widgets.TextInput(attrs=attrs), #Address Line 2
            widgets.TextInput(attrs=attrs), #City
            widgets.TextInput(attrs=attrs), #State
            widgets.TextInput(attrs=attrs), #Zip
            )
        super(AddressWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if not value:
            return [None, None, None, None, None]
        return [value.address_1, value.address_2,
                value.city, value.state, value.zip]

    def format_output(self, rw):
        rw.insert(0, '<label for="id_address_field_0">Address Line 1:</label>')
        rw.insert(2, '<label for="id_address_field_0">Address Line 2:</label>')
        rw.insert(4, '<label for="id_address_field_1">City:</label>')
        rw.insert(6, '<label for="id_address_field_1">State:</label>')
        rw.insert(8, '<label for="id_address_field_2">Zip Code:</label>')
        return u''.join(rw)
