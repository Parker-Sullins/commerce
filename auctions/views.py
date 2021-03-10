from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from . import forms


def index(request):
    return render(request, "auctions/index.html", {"listings": Listing.objects.all()})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {"message": "Invalid username and/or password."})
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {"message": "Passwords must match."})

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {"message": "Username already taken."})
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, listing_id):
    listings = Listing.objects.get(id=listing_id)
    comments = listings.comments.all()
    listing_author = listings.author
    close_listing_button = False
    if listing_author == request.user and listings.active_listing:
        close_listing_button = True
    top_bid_object = highest_bidder(listing_id=listing_id)
    if request.method == "GET":
        return render(request, "auctions/listing.html", {"listings": listings, "close_ls_button": close_listing_button,
                                                         "comments": comments, "bids": top_bid_object,
                                                         "list": listing_author})
    else:
        pass


def create_listing(request):
    if request.method == "GET":
        form = forms.CreateListing()
        return render(request, "auctions/create_listing.html", {"form": form})
    else:
        form = forms.CreateListing(request.POST, request.FILES)
        if form.is_valid():
            listing_instance = form.save(commit=False)
            listing_instance.author = request.user
            listing_instance.save()
            return HttpResponseRedirect(reverse("auctions:index"))
        elif ValidationError:
            form = forms.CreateListing()
            return render(request, "auctions/create_listing.html", {"form": form,
                                                                    "error": 'Price Must Be Between $0.00 and $10,000'})


def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.active_listing = False
    listing.save()
    return HttpResponseRedirect(reverse("auctions:listing", args=(listing_id,)))


def category(request):
    return render(request, 'auctions/category.html')


def comment(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(id=listing_id)
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment_instance = form.save(commit=False)
            comment_instance.comment_author = request.user
            comment_instance.listing = listing
            comment_instance.save()
            return HttpResponseRedirect(reverse("auctions:index"))


def add_comment(request, listing_id):
    if request.method == 'POST':
        listings = Listing.objects.get(id=listing_id)
        form = forms.CommentForm()
        return render(request, "auctions/comment.html", {"form": form, "listings": listings})


def bid(request, listing_id):
    if request.method == 'POST':
        form = forms.PlaceBidForm(request.POST)
        if form.is_valid():
            top_bidder = highest_bidder(listing_id=listing_id)
            if top_bidder:
                top_bidder = top_bidder.bid_price
            else:
                top_bidder = 0
            bid_offer = form.cleaned_data['bid_price']
            listing = Listing.objects.get(pk=listing_id)
            if bid_offer > (top_bidder or listing.price):
                    bid_instance = form.save(commit=False)
                    bid_instance.bid_author = request.user
                    bid_instance.listing = listing
                    bid_instance.save()
                    return HttpResponseRedirect(reverse("auctions:index"))
            else:
                error = "Bid Must Be Greater Than The Current Bid"
                listings = Listing.objects.get(id=listing_id)
                form = forms.PlaceBidForm()
                return render(request, "auctions/place_bid.html", {"form": form, "listings": listings, "error": error})


def highest_bidder(listing_id=None):
    listings = Listing.objects.get(id=listing_id)
    bids = listings.bid_listing.all()
    highest_bid = 0
    top_bidder = None
    for bid in bids:
        instance_bid = bid.bid_price
        if instance_bid > highest_bid:
            highest_bid = instance_bid
            top_bid_id = bid.id
            top_bidder = listings.bid_listing.get(pk=top_bid_id)
            continue
    return top_bidder


def place_bid(request, listing_id, error=None):
    if request.method == 'POST':
        listings = Listing.objects.get(id=listing_id)
        form = forms.PlaceBidForm()
        return render(request, "auctions/place_bid.html", {"form": form, "listings": listings})
    else:
        listings = Listing.objects.get(id=listing_id)
        form = forms.PlaceBidForm()
        return render(request, "auctions/place_bid.html", {"form": form, "listings": listings, "error": error})


def current_bids(request):
    username = request.user.username
    if request.method == "GET":
        user = User.objects.get(pk=request.user.id)
        current_bids = user.bid_author.all()
        return render(request, "auctions/current_bids.html", {"username": username, "current_bids": current_bids})
    else:
        pass


@login_required
def watchlist(request):
    if request.method == 'GET':
        #What ->
        user = User.objects.get(pk=request.user.id)
        watch_list_items = user.watch_list_item.all()
        return render(request, "auctions/watchlist.html", {"watch_list_items": watch_list_items})
    else:
        # Could refactor add_watch_list to be be a post method for watchlist?
        pass


def add_watch_list(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=listing_id)
        listing.watch_list_item.add(request.user)
        return HttpResponseRedirect(reverse("auctions:index"))


# def delete_watch_list(request):
