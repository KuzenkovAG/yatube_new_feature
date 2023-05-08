from django import forms


class ValidateTextFieldMixin:
    """Validate text field of Form."""
    def clean_text(self):
        data = self.cleaned_data['text']
        if data is None:
            raise forms.ValidationError('Вы должны заполнить поле текст')
        return data
