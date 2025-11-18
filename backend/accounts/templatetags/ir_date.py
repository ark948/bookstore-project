from django import template

from convertdate import persian

register = template.Library()

@register.filter(expects_localtime=True)
def to_persian(dt):
    """Converts datetime object to represent persian date and time."""
    return persian.from_gregorian(
        int(dt.strftime("%Y")), int(dt.strftime("%m")), int(dt.strftime("%d"))
    )