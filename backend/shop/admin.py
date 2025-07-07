from django.contrib import admin

# Register your models here.

from .models import (
    Country,
    Language,
    Translator,
    Illustrator,
    Author,
    Genre,
    Tag,
    Keyword,
    Publication,
    OriginalLanguage,
    Format,
    Size,
    Series,
    AgeRecommendation,
    Book,
    Award,
    Review,
    Discount,
    Comment,
    Order,
    Payment,
    Invoice,
)


admin.site.register(Country)
admin.site.register(Language)
admin.site.register(Illustrator)
admin.site.register(Translator)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(Keyword)
admin.site.register(Publication)
admin.site.register(OriginalLanguage)
admin.site.register(Format)
admin.site.register(Size)
admin.site.register(Series)
admin.site.register(AgeRecommendation)
admin.site.register(Book)
admin.site.register(Award)
admin.site.register(Review)
admin.site.register(Discount)
admin.site.register(Comment)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Invoice)