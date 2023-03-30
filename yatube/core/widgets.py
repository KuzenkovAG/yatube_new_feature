from django import forms


class DateForm(forms.DateInput):
    input_type = 'text'
