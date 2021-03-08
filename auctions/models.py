from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass


class Listing(models.Model):
    owner = models.CharField(max_length=30, default='Owner')
    title = models.CharField(max_length=60, default='Title')
    description = models.TextField(default='Description')
    image = models.ImageField(upload_to='auctions/images/', default='auctions/images/default.png')
    price = models.IntegerField(default=0)
    category = models.CharField(max_length=45, default='Category')
    listing_date = models.DateField("Date", default=datetime.date.today)

    def __str__(self):
        return f"{self.owner} : {self.title} ... price: {self.price}"


class Bid(models.Model):
    listing_id = models.IntegerField(default=0000)
    bid_owner = models.CharField(max_length=30, default='Bid Owner')
    bid_price = models.IntegerField(default=0)
    bid_date = models.DateField("Date", default=datetime.date.today)

    def __str__(self):
        return f"{self.bid_owner}...Bid Date: {self.bid_date} ... price: {self.bid_price}"


class Comment(models.Model):
    listing_id = models.IntegerField(default=0000)
    comment_owner = models.CharField(max_length=30, default='Comment Owner')
    comment_content = models.CharField(max_length=150, default='Comment')
    comment_date = models.DateField("Date", default=datetime.date.today)

    def __str__(self):
        return f"{self.comment_owner}...comment Date: {self.comment_date}"


class ClosedBid(models.Model):
    listing_id = models.IntegerField(default=0000)
    closed_bid_owner = models.CharField(max_length=30, default='Bid Owner')
    closed_bid_winner = models.CharField(max_length=30, default='Bid Winner')
    closed_bid_price = models.IntegerField(default=0)
    closed_bid_date = models.DateField("Date", default=datetime.date.today)

    def __str__(self):
        return f"Original Owner:{self.closed_bid_owner}...Bid Winner: {self.closed_bid_winner} \
        ...Winning Bid Price: {self.closed_bid_price}...Date: {self.closed_bid_date}"
