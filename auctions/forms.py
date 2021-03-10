from django import forms
from . import models


class CreateListing(forms.ModelForm):
    class Meta:
        model = models.Listing
        fields = ['title', 'description', 'image', 'price', 'category']


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['comment_content']


class PlaceBidForm(forms.ModelForm):
    class Meta:
        model = models.Bid
        fields = ['bid_price']
