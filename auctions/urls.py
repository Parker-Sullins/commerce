from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("current_bids", views.current_bids, name="current_bids"),
    path("watchlist/add_watch_list/<int:listing_id>", views.add_watch_list, name="add_watch_list"),
    path("listing/<int:listing_id>/add_comment", views.add_comment, name="add_comment"),
    path("listing/<int:listing_id>/comment", views.comment, name="comment"),
    path("listing/<int:listing_id>/place_bid", views.place_bid, name="place_bid"),
    path("listing/<int:listing_id>/bid", views.bid, name="bid"),
    path("listing/<int:listing_id>/close_listing", views.close_listing, name="close_listing"),
    path("categories", views.category, name="category")



]
