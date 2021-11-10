from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import UserManager


class CustomUser(AbstractUser):
    birthday = models.DateField(null=True, blank=True)
    CHOICES = {("male", "Male"), ("female", "Female")}
    gender = models.CharField(max_length=10, null=True, blank=True, choices=CHOICES)
    country = CountryField(blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r"^\+(?:[0-9]●?){6,14}[0-9]$",
        message=_(
            "Enter a valid international mobile phone number starting with +(country code)"
        ),
    )
    mobile_phone = models.CharField(
        validators=[phone_regex],
        verbose_name=_("Mobile phone"),
        max_length=17,
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        verbose_name=_("Photo"),
        upload_to="photos/",
        default="photos/default-user-avatar.png",
    )

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    username = None

    email = models.EmailField("email address", blank=False, null=False, unique=True)

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        """Returns the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""

        send_mail(subject, message, from_email, [self.email], **kwargs)


class Product(models.Model):
    #  to=CustomUser
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    title = models.CharField(max_length=300, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to="product/%Y/%m/%d", null=True, blank=True)
    brand = models.CharField(max_length=300, null=True, blank=True)
    category = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    SIZE_CHOICE = (
        ("m", "M"),
        ("l", "L"),
        ("xl", "XL"),
    )

    size = models.CharField(max_length=10, choices=SIZE_CHOICE, null=True, blank=True)

    tags = TaggableManager()

    rating = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    numbersOfReview = models.IntegerField(null=True, blank=True, default=0)
    countInStock = models.IntegerField(null=True, blank=True)
    isOutOfStock = models.BooleanField(default=False)
    isAvailable = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

    def get_absolute_url(self):
        return "/product/%i/" % self._id


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(
        to=CustomUser, on_delete=models.SET_NULL, null=True, blank=True
    )

    fullName = models.CharField(max_length=300, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    reviewImage = models.ImageField(upload_to="review/%Y/%m/%d", null=True, blank=True)

    feedback = models.TextField(
        help_text="Please share your feedback about the product Was the product as described? What is the quality like?",
        null=True,
        blank=True,
    )
    riderReview = models.TextField(
        help_text="How was your overall experience with our rider?",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.user)


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    shippingPrice = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    totalPrice = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )

    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=True)

    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(auto_now_add=True)

    isReturns = models.BooleanField(default=False)

    orderCreated = models.DateTimeField(auto_now_add=True)

    STATUS = (
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Out for delivery", "Out for delivery"),
        ("Delivered", "Delivered"),
    )
    status = models.CharField(max_length=200, null=True, blank=True, choices=STATUS)

    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.user)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)

    productTitle = models.CharField(max_length=300, null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    image = models.ImageField(upload_to="product/%Y/%m/%d", null=True, blank=True)

    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.productTitle


class shippingAddress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=300, null=True, blank=True)
    country = CountryField()
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True
    )

    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.address
