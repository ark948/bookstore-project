from django import forms

# Create your forms here

from .models import Book, Author

class NewBookForm(forms.ModelForm):
    title = forms.CharField(label="عنوان", max_length=256, required=True)

    authors = forms.ModelMultipleChoiceField(
        label="نویسندگان",
        queryset=Author.objects.all(),
    )

    class Meta:
        model = Book
        fields = (
            'title',
            'authors',
        )