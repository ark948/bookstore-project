from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from time import timezone

from accounts.models import CustomUser

# Create your models here.

# checks:
# ALL models must be Capitalized (DONE)
# ALL models must be singular (DONE)
# ALL fields must be lowercased using underscores, not camelCase (full_name, NOT fullName) (DONE)
# Provide Verbose name for all non-relation fields (otherwise django will do it itself but with its own ways)
# Provide related_name for all relation fields
# Provide verbose_name and verbose_name_plural for model itself (by using class Meta)
# Provide ordering to Meta, ONLY IF NECESSARY (IT WILL AFFECT PERFORMANCE)
# Provide index if necessary
# FIX all choice fields (dicts are faster for key related lookups)
# Add get_<modelName>_display for all choice fields (a human-readable version) CANCELLED, it is automatically provided by django
# add null=True and blank=True (null for database, blank is for validation)
# EXAMPLE: if blank is true, then a form will allow empty value
# if a null is required for CharField or TextField, DO NOT USE Null, use default="" and blank=True instead
# EXCEPTION: if a CharField has both unique=True and blank=True, then null=True is required
# NULL value for relationships (mostly one to one)
# At least one unique (required value) for each table
# Configure image field for book's cover image (static location)


# Inherit this to use created_at and updated_at
class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        abstract = True


class Country(models.Model):
    name = models.CharField("Country Name", max_length=128, blank=False, null=False)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ["name"]
    
    def __str__(self) -> str:
        return f"[CountryObj] {self.name}"
    

class Translator(models.Model):
    pen_name = models.CharField("Pen Name", max_length=128, blank=True, null=True)
    first_name = models.CharField("First Name", max_length=128)
    last_name = models.CharField("Last Name", max_length=128)
    email = models.EmailField("Email", blank=True, null=True)
    dob = models.DateField("Date of Birth", blank=True, null=True)
    book_count = models.PositiveSmallIntegerField("Number of Books")
    nationality = models.ForeignKey(Country, models.DO_NOTHING, related_name='translators', verbose_name="Nationality") # country.translators.all()

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return None
        
    def __str__(self) -> str:
        return f"[TranslatorObj] {self.pk}"


class Illustrator(models.Model):
    pen_name = models.CharField("Pen Name", max_length=128, blank=True, null=True)
    first_name = models.CharField("First Name", max_length=128)
    last_name = models.CharField("Last Name", max_length=128)
    email = models.EmailField("Email", blank=True, null=True)
    dob = models.DateField("Date of Birth", blank=True, null=True)
    book_count = models.PositiveSmallIntegerField("Number of Books")
    nationality = models.ForeignKey(Country, models.DO_NOTHING, related_name='illustrators', verbose_name="Nationality") # country.illustrators.all()

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return None
        
    def __str__(self) -> str:
        return f"[IllustratorObj] {self.pk}"


class Author(models.Model):
    first_name = models.CharField("First Name", max_length=128)
    last_name = models.CharField("Last Name", max_length=128)
    email = models.EmailField("Email", blank=True, null=True)
    dob = models.DateField("Date of Birth", blank=True, null=True)
    book_count = models.PositiveSmallIntegerField("Number of Books")
    nationality = models.ForeignKey(Country, models.DO_NOTHING, related_name='authors', verbose_name="Nationality") # country.authors.all()

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return None

    def __str__(self) -> str:
        return f"[AuthorObj] {self.pk}"

class Genre(models.Model):
    title = models.CharField("Title", max_length=64, blank=False, null=False, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return f"[GenreObj] {self.title}"

class Publication(models.Model):
    title = models.CharField("Title", max_length=128)
    book_count = models.PositiveSmallIntegerField("Number of Books")
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, related_name='publications', verbose_name="Based in") # Country.publications.all()
    url = models.URLField(verbose_name="Publication's Website", blank=True)


class Language(models.Model):
    name = models.CharField("Name", max_length=128)
    book_count = models.PositiveSmallIntegerField("Number of Books")


class Format(models.Model):
    BOOK_FORMATS = {
        'HC': "Hardcover",
        'PB': "Paperback"
    }
    name = models.CharField(max_length=64, choices=BOOK_FORMATS, default=BOOK_FORMATS["PB"])
    book_count = models.PositiveSmallIntegerField("Number of Books")


class Size(models.Model):
    BOOK_SIZES = {
        'SM': "Small",
        'MD': "Medium",
        'LG': "Large"
    }
    name = models.CharField(max_length=32, choices=BOOK_SIZES, default=BOOK_SIZES["MD"], verbose_name="Name of book size")

class Series(models.Model):
    name = models.CharField(max_length=128, verbose_name="Name of the series")
    book_count = models.PositiveSmallIntegerField("Number of Books in this series")


class Organization(models.Model):
    title = models.CharField(max_length=128, verbose_name="Organization's name")


class Award(BaseModel):
    AWARD_STATUSES = {
        "UN": "Unknown",
        "AC": "Active",
        "NC": "Inactive",
        "RV": "Revoked"
    }
    title = models.CharField(max_length=128, verbose_name="Title of the Award")
    issued_by = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, related_name='awards', verbose_name="Issued by")
    status = models.CharField(max_length=2, choices=AWARD_STATUSES, default=AWARD_STATUSES["UN"], verbose_name="Status of award")


class AgeRecommendation(models.Model):
    AGE_GROUPS = {
        "CHLD": "0-12", # Children
        "TNGS": "13-17", # Teenagers
        "YADL": "18-25", # Young adults
        "MADL": "26-39", # Mid adults
        "ELDR": "40-60" # Elderly adults
    }
    group = models.CharField(max_length=4, choices=AGE_GROUPS, default=AGE_GROUPS["YADL"], verbose_name="Age group")
        

class Book(BaseModel):
    title = models.CharField("Title", max_length=128, blank=False, null=False)
    authors = models.ManyToManyField(Author, related_name='books', through='BookAuthor', verbose_name="Author(s)")
    publisher = models.ForeignKey(Publication, related_name='books', verbose_name="Published by") # publisher.books.all()
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING, related_name='books', verbose_name="Language") # Language.books.all()
    original_language = models.ForeignKey(Language, verbose_name="Original language")
    edition = models.PositiveSmallIntegerField("Edition")
    page_count = models.IntegerField("Number of Pages")
    pub_date = models.DateField("Published on")
    format = models.ForeignKey(Format, verbose_name="Format") # hardcover, paperback, ebook, audio
    series = models.ForeignKey(Series, verbose_name="Belongs to series") # is this book part of a series
    ISBN = models.CharField("ISBN", blank=False, null=False)
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING, related_name="books", verbose_name="Genre") # Genre.books.all()
    price = models.DecimalField("Price")
    available = models.BooleanField("Available", default=False)
    copies_available = models.PositiveSmallIntegerField("In Stock")
    description = models.TextField("Description")
    summary = models.TextField(verbose_name="Summary")
    age_recommendation = models.ForeignKey(AgeRecommendation, on_delete=models.DO_NOTHING, null=True, verbose_name="Suitable for")
    keywords = models.CharField("Keywords")
    translator = models.ForeignKey(Translator, verbose_name="Translated by")
    illustrator = models.ForeignKey(Illustrator, verbose_name="Illustrated by")
    awards = models.ManyToManyField(Award, "Awards won")
    rating = models.SmallIntegerField("Rating", validators=[MinValueValidator(1), MaxValueValidator(10)])
    cover_image = models.ImageField("Cover Image")

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self) -> str:
        return f"[BookObj] {self.title}"
    
class Review(BaseModel):
    title = models.CharField("Title", max_length=64)
    content = models.TextField("Content")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews") # book.reviews.all()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews") # user.reviews.all()
    rating = models.SmallIntegerField(
            "Review Rating", 
            validators=[MinValueValidator(1), MaxValueValidator(10)]
        )
    vote = models.SmallIntegerField("Vote")


class Discount(models.Model):
    percentage = models.DecimalField()
    expiry = models.DateTimeField()


class Comment(BaseModel):
    body = models.CharField("Body", max_length=5000)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments") # book.comments.all()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments") # user.comments.all()


class OrderItem(models.Model):
    books = models.ManyToManyField(Book)
    items_count = models.PositiveSmallIntegerField(
        "Total Number of Items",
        validators=[MaxValueValidator(50)]
    )
    total_price = models.DecimalField()


class Order(BaseModel):
    ORDER_STATUSES = (
        ("PENDING-PAYMENT", "Pending payment"),
        ("CONFIRMED", "Confirmed"),
        ("PROCESSING", "Processing"),
        ("SHIPPED", "Shipped"),
        ("CANCELLED", "Cancelled")
    )
    customer_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders') # CustomUser.orders.all()
    order_items = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=ORDER_STATUSES, default=ORDER_STATUSES[2], verbose_name="Status of order")

    class Meta:
        unique_together = (
            'customer_id',
            'order_items'
        )

    def __str__(self) -> str:
        return f"[OrderObj] {self.pk}"


class Payment(BaseModel):
    customer_id = models.ForeignKey(CustomUser)
    order_id = models.ForeignKey(Order)

    class Meta:
        unique_together = (
            'customer_id',
            'order_id'
        )


class Invoice(BaseModel):
    order_id = models.ForeignKey(Order)
    payment_id = models.ForeignKey(Payment)

    class Meta:
        unique_together = (
            'order_id',
            'payment_id'
        )


# Association tables

class BookAuthor(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    # author_order = models.IntegerField()
    role = models.CharField(max_length=64, blank=True, verbose_name="Role")