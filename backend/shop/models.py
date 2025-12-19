from django.db import models
from django.contrib import admin
from django.db.models import Q, CheckConstraint
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
import datetime
from accounts.models import CustomUser

# Create your models here.

# NOTE: for notes and some info on this database design, refer to note.txt

# Inherit this to use created_at and updated_at
class TimeStampModel(models.Model):
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    class Meta:
        abstract = True


class Country(models.Model):
    name = models.CharField("Country Name", max_length=128, blank=False, null=False)

    class Meta:
        ordering = ["name"]
        verbose_name = "Country"
        verbose_name_plural = "Countries"
    
    def __str__(self) -> str:
        return self.name
    

class Contributor(models.Model):
    pen_name = models.CharField("Pen Name", max_length=128, blank=True, default="")
    fa_name = models.CharField("Name (fa)", max_length=128, blank=True, default="")
    en_name = models.CharField("Name (en)", max_length=128, blank=True, default="")
    email = models.EmailField("Email", blank=True, null=True)
    dob = models.DateField("Date of Birth", blank=True, null=True)
    

class Translator(Contributor):
    nationality = models.ForeignKey(
        verbose_name="Nationality", 
        to=Country, 
        null=True, 
        on_delete=models.SET_NULL, 
        related_name='translators'
    ) # <CountryObj>.translators.all()
    
    @property
    def books_count(self) -> int:
        return self.books.count()

    @property
    def full_name(self) -> str:
        return self.fa_name
        
    def __str__(self) -> str:
        if self.pen_name:
            return self.pen_name
        elif self.fa_name:
            return self.fa_name
        else:
            return f"[TranslatorObj] {self.pk}"


class Illustrator(Contributor):
    nationality = models.ForeignKey(
        verbose_name="Nationality", 
        to=Country, 
        null=True, 
        on_delete=models.SET_NULL, 
        related_name='illustrators'
    ) # <CountryObj>.illustrators.all()

    @property
    def books_count(self) -> int:
        return self.books.count()

    @property
    def full_name(self) -> str:
        return self.fa_name
        
    def __str__(self) -> str:
        return f"[IllustratorObj] {self.pk}"


class Author(Contributor):
    nationality = models.ForeignKey(
        verbose_name="Nationality", 
        to=Country, 
        null=True, 
        on_delete=models.SET_NULL, 
        related_name='authors'
    ) # <CountryObj>.authors.all()

    @property
    def books_count(self) -> int:
        return self.books.count()

    @property
    def full_name(self) -> str:
        if self.pen_name:
            return self.pen_name
        elif self.en_name:
            return self.en_name
        elif self.fa_name:
            return self.fa_name
        else:
            return f"[<AuthorObj> {self.pk}]"

    def __str__(self) -> str:
        if self.pen_name:
            return self.pen_name
        elif self.en_name:
            return self.en_name
        elif self.fa_name:
            return self.fa_name
        else:
            return f"[<AuthorObj> {self.pk}]"


class Genre(models.Model):
    title = models.CharField("Title", max_length=64, blank=False, unique=True)

    class Meta:
        ordering = ("title",)

    @property
    def books_count(self) -> int:
        return len(self.books.all())

    def __str__(self) -> str:
        return self.title
    

class Tag(models.Model):
    name = models.CharField("Name", max_length=64, blank=False, unique=True)

    def __str__(self) -> str:
        return self.name


class Keyword(models.Model):
    name = models.CharField("Name", max_length=64, blank=False, unique=True)

    def __str__(self) -> str:
        return self.name


class Publication(models.Model):
    title = models.CharField("Title", max_length=128, blank=False)
    country = models.ForeignKey(
            verbose_name="Based in", 
            to=Country, null=True, 
            on_delete=models.SET_NULL, 
            related_name='publications'
        ) # <CountryObj>.publications.all()
    url = models.URLField("Publication's Website", blank=True)

    @property
    def books_count(self) -> int:
        return len(self.books.all())

    def __str__(self) -> str:
        return self.title


class Language(models.Model):
    name = models.CharField("Name", max_length=128, unique=True)

    @property
    def get_books_count_current_language(self) -> int:
        return len(self.current_books.all())
    
    @property
    def get_books_count_original_language(self) -> int:
        return len(self.original_books.all())

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Size(models.Model):
    BOOK_SIZES = {
        'SM': "Small",
        'MD': "Medium",
        'LG': "Large"
    }
    name = models.CharField("Name of book size", max_length=32, choices=BOOK_SIZES, default=BOOK_SIZES["MD"])


class Series(models.Model):
    name = models.CharField("Name of the series", max_length=128, blank=True, default="")

    class Meta:
        verbose_name = "Series"
        verbose_name_plural = "Series"

    def __str__(self) -> str:
        return self.name


class Organization(models.Model):
    title = models.CharField("Organization's name", max_length=128, blank=True, default="Unknown")

    def __str__(self) -> str:
        return self.title


def get_year_choices():
    current_year = datetime.date.today().year
    return [(r, r) for r in range(1900, current_year + 1)]
        

class Book(TimeStampModel):
    
    BOOK_FORMATS = {
        'hardcover': "Hardcover",
        'paperback': "Paperback"
    }
    AGE_GROUPS = {
        "Unavailable": "0-0",
        "Children": "0-12",
        "Teenagers": "13-17",
        "Young Adults": "18-25",
        "Adults": "26-39",
        "Elderly": "40-60"
    }
    title = models.CharField("Title", max_length=256, blank=False, db_index=True)
    authors = models.ManyToManyField(Author, related_name="books")
    publisher = models.ForeignKey(
            verbose_name="Published by", 
            to=Publication, 
            null=True,
            on_delete=models.SET_NULL, 
            related_name='books'
        ) # <PublisherObj>.books.all()
    language = models.ForeignKey(
            verbose_name="Language", 
            to=Language, 
            null=True, 
            on_delete=models.SET_NULL, 
            related_name='current_books'
        ) # <LanguageObj>.books.all()
    original_language = models.ForeignKey(
            verbose_name="Original language",
            to=Language, 
            null=True,
            on_delete=models.SET_NULL,
            related_name="original_books"
        ) # <OriginalLanguageObj>.books.all()
    edition = models.PositiveSmallIntegerField("Edition", blank=True, null=True)
    page_count = models.IntegerField("Number of Pages")
    pub_date = models.IntegerField("Publication Year",choices=get_year_choices(), default=datetime.date.today().year)
    format = models.CharField(verbose_name="Format", choices=BOOK_FORMATS, null=False, blank=False, default=BOOK_FORMATS["paperback"])
    series = models.ForeignKey(verbose_name="Belongs to series", null=True, on_delete=models.SET_NULL, to=Series, related_name='books', blank=True) # <SeriesObj>.books.all()
    ISBN = models.CharField("ISBN", blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name="books")
    tags = models.ManyToManyField(Tag, blank=True)
    price = models.DecimalField("Price", validators=[MinValueValidator(0)], blank=False, null=False, decimal_places=3, max_digits=12, default=0)
    available = models.BooleanField("Available", default=False)
    copies_available = models.PositiveSmallIntegerField("In Stock", blank=True, null=True, default=0)
    description = models.TextField("Description", blank=True, default="")
    summary = models.TextField("Summary", blank=True, default="")
    age_recommendation = models.CharField("Age recommended for", choices=AGE_GROUPS, null=False, default=AGE_GROUPS["Unavailable"])
    keywords = models.ManyToManyField(Keyword, blank=True)
    translators = models.ManyToManyField(Translator, blank=True, related_name='books')
    illustrators = models.ManyToManyField(Illustrator, blank=True, related_name='books')
    rating = models.PositiveSmallIntegerField("Rating", validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, blank=True)
    cover_image = models.ImageField("Cover Image", upload_to='images/', null=True, blank=True)

    class Meta:
        ordering = ("title",)
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self) -> str:
        return f"{self.title}_{self.pk}"
    

class Award(TimeStampModel):
    AWARD_STATUSES = {
        "UN": "Unknown",
        "AC": "Active",
        "NC": "Inactive",
        "RV": "Revoked"
    }
    title = models.CharField("Title of the Award", max_length=128, blank=True, default="")
    issued_by = models.ForeignKey(verbose_name="Issued by", to=Organization, on_delete=models.SET_DEFAULT, related_name='awards', default="Unknown") # <OrganizationObj>.awards.all()
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
    percentage = models.DecimalField("Percentage", decimal_places=2, max_digits=4)
    expiry = models.DateTimeField("Expires on")


class Comment(TimeStampModel):
    STATUS_CHOICES = {
        "P": "Pending",
        "A": "Approved",
        "R": "Rejected"
    }
    title = models.CharField("Title", max_length=60, null=True, blank=True)
    body = models.CharField("Body", max_length=500)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments") # <BookObj>.comments.all()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments") # <CustomUserObj>.comments.all()
    anonymous = models.BooleanField("َAnonymous Comment", default=False, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="Pending")
    positive_votes = models.IntegerField("Positive Votes", default=0)
    negative_votes = models.IntegerField("Negative Votes", default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['book', 'user'], name='unique_book_user_comment')
        ]


class Vote(models.Model):
    # (actual_value_stored_in_db, human_readable_label)
    VOTE_CHOICES = ( 
        (1, "Upvote"),
        (-1, "Downvote"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='votes')
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'comment'], name='unique_user_comment_vote')
        ]


def generate_order_number():
    return uuid.uuid4().hex[:12].upper()


class Order(TimeStampModel):
    ORDER_STATUSES = {
        "PENDING": "Pending Payment",
        "CONFIRM": "Confirmed",
        "PROCESS": "Processing",
        "SHIPPED": "Shipped",
        "CANCELLED": "Cancelled"
    }
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders') # <CustomUserObj>.orders.all()
    status = models.CharField("Status of order", max_length=32, choices=ORDER_STATUSES, default=ORDER_STATUSES['PENDING'])
    order_number = models.CharField(unique=True, editable=False, default=generate_order_number)
    total_price = models.DecimalField(decimal_places=3, max_digits=12, default=0)

    def __str__(self) -> str:
        return f"[OrderObj] {self.pk}"
    

class OrderItem(TimeStampModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True) # a book can be in more than one cart, as long as copies_available > 1
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='items') # Order.items.all()
    item_count = models.PositiveSmallIntegerField(
        "Total number of this item",
        validators=[MaxValueValidator(4)],
        default=1
    )
    total_price = models.DecimalField("Total Price", decimal_places=3, max_digits=12)


class Payment(TimeStampModel):
    PAYMENT_STATUSES = {
        'PENDING': "Pending",
        'SUCCESS': "Successful",
        'FAILED': "Failure",
        'EXPIRE': "Expired"
    }
    customer = models.ForeignKey(CustomUser, related_name='payments', on_delete=models.CASCADE) # <CustomUserObj>.payments.all()
    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE) # <OrderObj>.payments.all()
    status = models.CharField("Payment's status", choices=PAYMENT_STATUSES, default=PAYMENT_STATUSES['PENDING'])

    class Meta:
        unique_together = (
            'customer',
            'order'
        )


class Invoice(TimeStampModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='invoices')
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='invoices')
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='invoices')


class Favorite(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            'user_id',
            'book_id'
        )

# Association tables
# NOTE: Objects need to ba creatd explicitly

# BookAuthor removed
# BookGenre removed
# BookTranslator removed
# BookTag removed
# BookIllustrator removed
# BookKeyword removed