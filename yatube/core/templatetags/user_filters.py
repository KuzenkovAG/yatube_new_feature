from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """Add HTML attribute 'class' to field."""
    return field.as_widget(attrs={'class': css})


@register.filter
def protect_mail(email):
    """Hide part of mail."""
    index = email.index('@')
    return email[:1] + '*****' + email[index:]
