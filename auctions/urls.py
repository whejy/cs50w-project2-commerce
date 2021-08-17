from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("new", views.new, name="new"),
    path("mylistings", views.mylistings, name="mylistings"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("listing<int:listing_id>", views.listing, name="listing"),
    path("bid", views.bid, name="bid"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
