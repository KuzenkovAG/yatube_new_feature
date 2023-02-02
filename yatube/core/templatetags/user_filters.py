from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """Add HTML attribute 'class' to field."""
    return field.as_widget(attrs={'class': css})


@register.filter
def protect_mail(email):
    index = email.index('@')
    len_short_mail = len(email[:index])
    if len_short_mail >= 5:
        return email[:1] + '***' + email[index-1:]
    return email[:1] + '***' + email[index:]
