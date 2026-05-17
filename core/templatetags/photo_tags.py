from django import template

register = template.Library()


@register.filter
def photo_url_or_none(field):
    try:
        if field and field.name:
            return field.url
    except Exception:
        pass
    return None
