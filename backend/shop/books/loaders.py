from dal import autocomplete

from shop.models import Author, Publication, Genre, Language


class AuthorsAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Author.objects.all().order_by('fa_name', 'en_name')
        if self.q:
            qs = qs.filter(en_name__istartswith=self.q)
        return qs
    
class PublishersAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Publication.objects.all().order_by('title')
        if self.q:
            qs = qs.filter(title__istartswith=self.q)
        return qs
    
class GenresAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):        
        qs = Genre.objects.all()
        if self.q:
            qs = qs.filter(title__istartswith=self.q)
        return qs
    
class LanguageAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Language.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs