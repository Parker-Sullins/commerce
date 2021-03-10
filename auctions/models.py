from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    pass


class Listing(models.Model):
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name="author")
    title = models.CharField(max_length=60, default=None)
    description = models.TextField(default=None)
    image = models.ImageField(upload_to='auctions/images/', default='auctions/images/default.png')
    price = models.IntegerField(default=None, validators=[MinValueValidator(0), MaxValueValidator(10000)])
    category = models.CharField(max_length=45, default=None)
    listing_date = models.DateField("Date", default=datetime.date.today)
    watch_list_item = models.ManyToManyField(User, blank=True, related_name="watch_list_item")
    active_listing = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.author} : {self.title} ... price: {self.price}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None, related_name='bid_listing')
    bid_author = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name="bid_author")
    bid_price = models.IntegerField(default=0)
    bid_date = models.DateField("Date", default=datetime.date.today)

    def __str__(self):
        return f"{self.bid_author}...Bid Date: {self.bid_date} ... price: {self.bid_price}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default=None, related_name='comments')
    comment_author = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name="comment_author")
    comment_content = models.CharField(max_length=150, blank=False, null=False)
    comment_date = models.DateField("Date", default=datetime.date.today)

    def __str__(self):
        return f"{self.comment_author}...comment Date: {self.comment_date}"



