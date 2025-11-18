from django import template

from convertdate import persian

register = template.Library()

@register.filter(expects_localtime=True)
def to_persian(dt):
    """Converts datetime object to represent persian date and time."""
    date = persian.from_gregorian(
        int(dt.strftime("%Y")), int(dt.strftime("%m")), int(dt.strftime("%d"))
    )
    year = date[0]
    month = None
    day = date[2]
    # These are persian months
    match date[1]:
        case 1:
            month = "فروردین"
        case 2:
            month = "اردیبهشت"
        case 3:
            month = "خرداد"
        case 4:
            month = "تیر"
        case 5:
            month = "مرداد"
        case 6:
            month = "شهریور"
        case 7:
            month = "مهر"
        case 8: 
            month = "آبان"
        case 9:
            month = "آذر"
        case 10:
            month = "دی"
        case 11:
            month = "بهمن"
        case 12:
            month = "اسفند"
        case _:
            month = "ERR"

    return f"{day} {month} {year}"