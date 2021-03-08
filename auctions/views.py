from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, listing_id):
    item = Listing.objects.get(id=listing_id)
    #Try listing_id if does not index raise 404
    if request.method == "GET":
        return render(request, "auctions/listing.html", {
            "item": item
        })
    else:
        pass

@login_required
def watchlist(request):
    if request.method == 'GET':
        username = request.user.username
        return render(request, "auctions/watchlist.html", {"username": username})
    else:
        #Post method for adding new listings to watchlist
        pass


def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create_listing.html")
    else:
        pass


def current_bids(request):
    username = request.user.username
    if request.method == "GET":
        return render(request, "auctions/current_bids.html", {"username": username})
    else:
        pass

