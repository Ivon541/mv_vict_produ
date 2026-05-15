# aut_app/forms.py
from django import forms

class TicketForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    asunto = forms.CharField(max_length=200)
    mensaje = forms.CharField(widget=forms.Textarea)