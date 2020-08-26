"""
    Created by Ma. Micah Encarnacion on 18/08/2020
"""
from django import forms


class RegisterUser(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email_address = forms.CharField()
    contact_number = forms.CharField()
    username = forms.CharField()
    password = forms.CharField()
