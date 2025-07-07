from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import time

from accounts.models import CustomUser

# Create your models here.

# checks:
# ------------------
# ALL models must be Capitalized (DONE)
# ALL models must be singular (DONE)
# ALL fields must be lowercased using underscores, not camelCase (full_name, NOT fullName) (DONE)
# Provide Verbose name for all non-relation fields (otherwise django will do it itself but with its own ways) (DONE)
# Provide related_name for all relation fields (DONE)
# Provide verbose_name and verbose_name_plural for model itself (by using class Meta) (DONE)
# Provide ordering to Meta, ONLY IF NECESSARY (IT WILL AFFECT PERFORMANCE)
# Models with ordering: (DONE)
    # Book (title)
    # Genre (name)
    # Country (name)
    # Language (name)
# Provide index if necessary: (DONE)
    # Index provided to Book
# FIX all choice fields (dicts are faster for key related lookups) (DONE)
# Rename manytomany fields to plural format such as genres field of Book model (DONE)
# Distinguish between DO_NOTHING and CASCADE in relation fields (DONE)
# NOTE: DO_NOTHING will cause integrity problems, best to choose something else (DONE)
# UPDATE all DO_NOTHING statements (DONE)
# add null=True and blank=True (null for database, blank is for validation) (DONE)
# EXAMPLE: if blank is true, then a form will allow empty value (DONE)
# if a null is required for CharField or TextField, DO NOT USE Null, use default="" and blank=True instead (DONE)
# Configure image field for book's cover image (static location) (DONE)

# Relationships to watch that may causes errors:
# Book - OrderItems (books field)


# Relationships
# ------------------
# Book M:N Author -> BookAuthor
# Book M:N Genres -> BookGenre
# Book M:N Tag -> BookTag
# Book M:N Translator -> BookTranslator
# Book M:N Illustrator -> BookIllustrator

# Book 1:N Award (CASCADE)
# Award 1:1 Book (DO_NOTHING)

# Book 1:1 Publication
# Publication 1:N Book

# Book 1:1 Format
# Format 1:N Book

# Book 1:1 Size
# Size 1:N Book

# Book 1:1 Series
# Series 1:N Book

# Book 1:1 Language
# Language 1:N Book

# Book 1:1 OriginalLanguage
# OriginalLanguage 1:N

# Book 1:1 AgeRecommendation
# AgeRecommendation 1:N Book

# Book 1:N Review (CASCADE)
# Review 1:1 Book (DO_NOTHING)

# Book 1:N Comment (CASCADE)
# Comment 1:1 Book (DO_NOTHING)

# Payment 1:1 Discount
# Discount 1:N Payment

# Organization 1:N Award
# Award 1:1 Organization

# Author 1:1 Country (nationality field)
# Translator 1:1 Country (nationality field)
# Illustrator 1:1 Country  (nationality field)

# Country 1:N Author
# Country 1:N Translator
# Country 1:N Illustrator

# Order 1:1 OrderItems
# Order 1:1 CustomUser
# Order 1:N Payment

# Payment 1:1 Order

# Payment n:n Invoice


# Inherit this to use created_at and updated_at
class TimeStampModel(models.Model):
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    class Meta:
        abstract = True


class Country(models.Model):
    name = models.CharField("Country Name", max_length=128, blank=False, null=False, default="Unknown")

    class Meta:
        ordering = ["name"]
        verbose_name = "Country"
        verbose_name_plural = "Countries"
    
    def __str__(self) -> str:
        return f"[CountryObj] {self.name}"
    

class Translator(models.Model):
    pen_name = models.CharField("Pen Name", max_length=128, blank=True, default="")
    first_name = models.CharField("First Name", max_length=128, blank=True, default="")
    last_name = models.CharField("Last Name", max_length=128, blank=True, default="")
    email = models.EmailField("Email", blank=True, null=True)
    dob = models.DateField("Date of Birth", blank=True, null=True)
    book_count = models.PositiveSmallIntegerField("Number of Books", blank=True, null=True)
    nationality = models.ForeignKey(verbose_name="Nationality", to=Country, on_delete=models.SET_DEFAULT, related_name='translators') # <CountryObj>.translators.all()

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return None
        
    def __str__(self) -> str:
        return f"[TranslatorObj] {self.pk}"


class Illustrator(models.Model):
    pen_name = models.CharField("Pen Name", max_length=128, blank=True, default="")
    first_name = models.CharField("First Name", max_length=128, blank=True, default="")
    last_name = models.CharField("Last Name", max_length=128, blank=True, default="")
    email = models.EmailField("Email", blank=True, null=True)
    dob = models.DateField("Date of Birth", blank=True, null=True)
    book_count = models.PositiveSmallIntegerField("Number of Books", blank=True, null=True)
    nationality = models.ForeignKey(verbose_name="Nationality", to=Country, on_delete=models.SET_DEFAULT, related_name='illustrators') # <CountryObj>.illustrators.all()

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return None
        
    def __str__(self) -> str:
        return f"[IllustratorObj] {self.pk}"


class Author(models.Model):
    pen_name = models.CharField("Pen Name", max_length=128, blank=True, default="")
    first_name = models.CharField("First Name", max_length=128, blank=True, default="")
    last_name = models.CharField("Last Name", max_length=128, blank=True, default="")
    email = models.EmailField("Email", blank=True, null=True)
    dob = models.DateField("Date of Birth", blank=True, null=True)
    book_count = models.PositiveSmallIntegerField("Number of Books", blank=True, null=True)
    nationality = models.ForeignKey(validators="Nationality", to=Country, on_delete=models.SET_DEFAULT, related_name='authors') # <AuthorObj>.authors.all()

    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return None

    def __str__(self) -> str:
        return f"[AuthorObj] {self.pk}"


class Genre(models.Model):
    title = models.CharField("Title", max_length=64, blank=False, unique=True)

    class Meta:
        ordering = ("title",)

    def __str__(self) -> str:
        return f"[GenreObj] {self.title}"
    

class Tag(models.Model):
    name = models.CharField("Name", max_length=64, blank=False, unique=True)


class Keyword(models.Model):
    name = models.CharField("Name", max_length=64, blank=False, unique=True)


class Publication(models.Model):
    title = models.CharField("Title", max_length=128, blank=False)
    book_count = models.PositiveSmallIntegerField("Number of Books from this publisher", blank=True, null=True)
    country = models.ForeignKey(verbose_name="Based in", to=Country, on_delete=models.SET_DEFAULT, related_name='publications') # <CountryObj>.publications.all()
    url = models.URLField("Publication's Website", blank=True)


class Language(models.Model):
    name = models.CharField("Name", max_length=128, unique=True)
    book_count = models.PositiveSmallIntegerField("Number of Books", blank=True, null=True)

    class Meta:
        ordering = ('name',)


class OriginalLanguage(Language):
    class Meta:
        ordering = ('name',)


class Format(models.Model):
    BOOK_FORMATS = {
        'hardcover': "Hardcover",
        'paperback': "Paperback"
    }
    name = models.CharField("Name", max_length=64, choices=BOOK_FORMATS, default=BOOK_FORMATS["paperback"])
    book_count = models.PositiveSmallIntegerField("Number of Books", blank=True, null=True)


class Size(models.Model):
    BOOK_SIZES = {
        'SM': "Small",
        'MD': "Medium",
        'LG': "Large"
    }
    name = models.CharField("Name of book size", max_length=32, choices=BOOK_SIZES, default=BOOK_SIZES["MD"])


class Series(models.Model):
    name = models.CharField("Name of the series", max_length=128, blank=True, default="")
    book_count = models.PositiveSmallIntegerField("Number of Books in this series", blank=True, null=True)

    class Meta:
        verbose_name = "Series"
        verbose_name_plural = "Series"


class Organization(models.Model):
    title = models.CharField("Organization's name", max_length=128, blank=True, default="Unknown")



class AgeRecommendation(models.Model):
    AGE_GROUPS = {
        "UNAV": "0-0", # Unavailable
        "CHLD": "0-12", # Children
        "TNGS": "13-17", # Teenagers
        "YADL": "18-25", # Young adults
        "MADL": "26-39", # Mid adults
        "ELDR": "40-60" # Elderly adults
    }
    group = models.CharField("Age group", max_length=4, choices=AGE_GROUPS, default=AGE_GROUPS["UNAV"])
        

class Book(TimeStampModel):
    title = models.CharField("Title", max_length=256, blank=False, db_index=True)
    authors = models.ManyToManyField(verbose_name="Author(s)", to=Author, through='BookAuthor', related_name='books')
    publisher = models.ForeignKey(verbose_name="Published by", to=Publication, related_name='books') # <PublisherObj>.books.all()
    language = models.ForeignKey(verbose_name="Language", to=Language, on_delete=models.SET_DEFAULT, related_name='books') # <LanguageObj>.books.all()
    original_language = models.ForeignKey(
            verbose_name="Original language", 
            to=OriginalLanguage, 
            related_name="books"
        ) # <OriginalLanguageObj>.books.all()
    edition = models.PositiveSmallIntegerField("Edition", blank=True, null=True)
    page_count = models.IntegerField("Number of Pages")
    pub_date = models.DateField("Published on", blank=True, null=True)
    format = models.ForeignKey(verbose_name="Format", to=Format, related_name='books') # <FormatObj>.books.all()
    series = models.ForeignKey(verbose_name="Belongs to series", to=Series, related_name='books') # <SeriesObj>.books.all()
    ISBN = models.CharField("ISBN", blank=True, null=True) # some books may not have ISBN
    genres = models.ManyToManyField(Genre, through="BookGenre") # related_name deleted
    tags = models.ManyToManyField(Tag, through="BookTag") # related_name not provided
    price = models.DecimalField("Price", validators=[MinValueValidator(0)], blank=True, null=True)
    available = models.BooleanField("Available", default=False)
    copies_available = models.PositiveSmallIntegerField("In Stock", blank=True, null=True)
    description = models.TextField("Description", blank=True, default="")
    summary = models.TextField("Summary", blank=True, default="")
    age_recommendation = models.ForeignKey(
            "Suitable for ages", 
            AgeRecommendation, 
            on_delete=models.SET_DEFAULT, 
            null=True, 
            related_name='books'
        ) # <AgeRecommendationObj>.books.all()
    keywords = models.ManyToManyField(Keyword, through="BookKeyword")
    translators = models.ManyToManyField(Translator, through="BookTranslator")
    illustrators = models.ManyToManyField(Illustrator, through="BookIllustrator")
    rating = models.PositiveSmallIntegerField("Rating", validators=[MinValueValidator(1), MaxValueValidator(10)])
    cover_image = models.ImageField("Cover Image", upload_to='images/')

    class Meta:
        ordering = ("title",)
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self) -> str:
        return f"[BookObj] {self.title}"
    

class Award(TimeStampModel):
    AWARD_STATUSES = {
        "UN": "Unknown",
        "AC": "Active",
        "NC": "Inactive",
        "RV": "Revoked"
    }
    title = models.CharField("Title of the Award", max_length=128, blank=True, default="")
    issued_by = models.ForeignKey("Issued by", Organization, on_delete=models.SET_DEFAULT, related_name='awards') # <OrganizationObj>.awards.all()
    status = models.CharField("Status of award", max_length=2, choices=AWARD_STATUSES, default=AWARD_STATUSES["UN"])
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='awards') # <BookObj>.awards.all()

    
class Review(TimeStampModel):
    title = models.CharField("Title", max_length=128)
    content = models.TextField("Content", max_length=1000)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews") # <BookObj>.reviews.all()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews") # <CustomUserObj>.reviews.all()
    rating = models.PositiveSmallIntegerField(
            "Review Rating", 
            validators=[MinValueValidator(1), MaxValueValidator(10)]
        )
    vote = models.SmallIntegerField("Vote")


class Discount(TimeStampModel):
    percentage = models.DecimalField("Percentage")
    expiry = models.DateTimeField("Expires on")


class Comment(TimeStampModel):
    body = models.CharField("Body", max_length=500)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments") # <BookObj>.comments.all()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments") # <CustomUserObj>.comments.all()


class OrderItem(TimeStampModel):
    books = models.ManyToManyField(Book) # a book can be in more than one cart, as long as copies_available > 1
    items_count = models.PositiveSmallIntegerField(
        "Total Number of Items",
        validators=[MaxValueValidator(50)]
    )
    total_price = models.DecimalField("Total Price")


class Order(TimeStampModel):
    ORDER_STATUSES = (
        ("pending payment", "Pending Payment"),
        ("confirmed", "Confirmed"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("cancelled", "Cancelled")
    )
    customer_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders') # <CustomUserObj>.orders.all()
    order_items_id = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    status = models.CharField("Status of order", max_length=32, choices=ORDER_STATUSES, default=ORDER_STATUSES[2])

    class Meta:
        unique_together = (
            'customer_id',
            'order_items'
        )

    def __str__(self) -> str:
        return f"[OrderObj] {self.pk}"


# An order may have more than one payment, for example, if one failed, we still want to keep the record of it
class Payment(TimeStampModel):
    PAYMENT_STATUSES = (
        ('pending', 'Pending')
        ('successful', "Successful"),
        ('failed', 'Failed'),
        ('expired', 'Expired')
    )
    customer_id = models.ForeignKey(CustomUser, related_name='payments') # <CustomUserObj>.payments.all()
    order_id = models.ForeignKey(Order, related_name='payments') # <OrderObj>.payments.all()
    status = models.CharField("Payment's status", choices=PAYMENT_STATUSES, default=PAYMENT_STATUSES[0])

    class Meta:
        unique_together = (
            'customer_id',
            'order_id'
        )

# Only successful payments can have invoices
# therefore, payment must have a status field
class Invoice(TimeStampModel):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            'order_id',
            'payment_id'
        )


# Association tables

class BookAuthor(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    # author_order = models.IntegerField() # Could be implemented later
    # role = models.CharField(verbose_name="Role", max_length=64, blank=True)


class BookGenre(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)
    # extra fields if required


class BookTag(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)


class BookTranslator(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    translator_id = models.ForeignKey(Translator, on_delete=models.CASCADE)


class BookIllustrator(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    illustrator_id = models.ForeignKey(Illustrator, on_delete=models.CASCADE)


class BookKeyword(models.Model):
    book_id = models.ForeignKey(Book, models.CASCADE)
    keyword_id = models.ForeignKey(Keyword, on_delete=models.CASCADE)