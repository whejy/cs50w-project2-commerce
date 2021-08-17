from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from decimal import Decimal

from .forms import NewListForm, NewBidForm
from .helpers import bidCheck, bidUpdate, unique
from .models import User, Listing, Bids, Comments, Watchlist, Winners
from .settings import STEP, CATEGORIES


@login_required(login_url="/bid")
def bid(request):
    form = NewBidForm(request.POST)
    if form.is_valid():
        bid = form.cleaned_data["bid"]
        listing_id = request.POST.get("listing_id")
        current_bid = bidCheck(listing_id)[0]
        if bid > current_bid:
            new_bid = Bids(
                user=User(id=request.user.id),
                item=Listing(id=listing_id),
                bid=bid
            )
            new_bid.save()
            messages.success(request, "Congratulations, you are the highest bidder!")
        else:
            messages.warning(request, "Your bid must be greater than the current bid.")
    return HttpResponseRedirect(f"listing{listing_id}" )


# Displays a list of all categories
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": CATEGORIES
    })


# Retrieves all items within a selected category
def category(request, category):
    empty = ""
    lst = []
    items = Listing.objects.filter(category=category)
    if not items:
        empty = f"Sorry, there are currently no listings in the '{category}' category."
    else:
        lst = bidUpdate(items)
    return render(request, "auctions/category.html", {
        "items": lst,
        "category": category,
        "empty": empty
    })


# Display listings the user is winning, has won, or has bid on but not currently winning
@login_required
def dashboard(request):
    won = []
    winning = []
    not_winning = []
    user = request.user
    items_won = Winners.objects.filter(
        winner=user,
    )
    bidded = Bids.objects.filter(
        user=User(id=request.user.id)
    )
    # If auction bidded on, but not won, update bid price and display to user
    if bidded:
        lst = []
        # Filter user's bids to only unique listings
        for item in bidded:
            lst.append(item.item.id)
        lst = unique(lst)
        for item_id in lst:
            # if user has bid on listing but listing is not in Winners table
            if not Winners.objects.filter(item=Listing(id=item_id)):
                current_bid = bidCheck(item_id)[0]
                winning_bidder = bidCheck(item_id)[1]
                product = Listing.objects.get(id=item_id)
                product.start_bid = current_bid
                # then user is either winning...
                if winning_bidder == user:
                    winning.append(product)
                    unique(winning)
                # or not currently winning the auction
                else:
                    not_winning.append(product)                     
    # If auction won, update winning bid price and display to user          
    if items_won:
        items = []
        for item in items_won:
            items.append(item.item)
        won = bidUpdate(items)

    data = {
        "Winning": winning,
        "Won": won,
        "Not Winning": not_winning
        }

    return render(request, "auctions/dashboard.html", {
        "data": data
    })


# Displays Active Listings page
def index(request):
    active_listings = []
    empty = ""
    listings = Listing.objects.all()
    items = bidUpdate(listings)    
    # exclude sold items
    for item in items:
        if not Winners.objects.filter(item=Listing(id=item.id)):
            active_listings.append(item)
    if not active_listings:
        empty = "Sorry, there are no active listings at this time."
    # notify user of any auctions they have won while logged out
    for items_sold in Winners.objects.all():
        if str(items_sold.winner) == str(request.user):
            if items_sold.notified == False:
                messages.success(request,
                    f"Congratulations! You won {items_sold.item.title} with a bid of ${items_sold.cost}!"
                    )
                items_sold.notified = True
                items_sold.save()
    return render(request, "auctions/index.html", {
        "listings": active_listings,
        "empty": empty
    })


# Retreive listing and determine watchlist-button display
def listing(request, listing_id):
    msg = ""
    remove = ""
    close = ""
    winning = ""
    watchlist = ""
    bid_label = "Current Bid: "
    user = request.user.id
    current_bid = bidCheck(listing_id)[0]
    # Catch for user accessing invalid listing via URL bar
    if current_bid == None:
        return HttpResponseRedirect(reverse("index"))

    form = NewBidForm(initial={
        'bid': STEP + float(current_bid)
        })
    in_watchlist = Watchlist.objects.filter(
        user=User(id=user),
        item=Listing(id=listing_id)
        )
    sellers_item = Listing.objects.filter(
        seller=User(id=user),
        id=listing_id
        )

    try:
        high_bidder = User.objects.get(username=bidCheck(listing_id)[1]).id
    except User.DoesNotExist:
        high_bidder = None
    try:
        closed = Winners.objects.get(item=Listing(id=listing_id))
    except Winners.DoesNotExist:
        closed = None
    try:
        winner = Winners.objects.get(item=Listing(id=listing_id))
    except Winners.DoesNotExist:
        winner = None

    if sellers_item:
        if closed:
            bid_label = "Final Bid: "
            msg = "You have closed this auction."
        else:
            close = "True"
            watchlist = "Close listing"
    elif in_watchlist:
        remove = "True"
        watchlist = "Remove from Watchlist"
    else:
        if closed:
            msg = "Sorry, this auction has ended."
        else:
            watchlist = "Add to Watchlist" 
    if high_bidder == user:
        winning = "True"
        if winner:
            bid_label = "Winning Bid: "
            msg = "Congratulations, you won this auction!"
        else:
            bid_label = "Your Bid: "
            msg = "You are the current the highest bidder!"
    if user == None:
        bid_label = "Current Bid: "
        msg = "You must be logged in to bid."
    return render(request, "auctions/listing.html", {
        "close": close,
        "closed": closed,
        "message": msg,
        "remove" : remove,
        "watchlist": watchlist,
        "winning": winning,
        "form": form,
        "bid": current_bid,
        "bid_label": bid_label,
        "listing": Listing.objects.get(id=listing_id)
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Display user's selling list and allow sellerr to close listing
@login_required(login_url='/mylistings')
def mylistings(request):
    user = request.user
    items = Listing.objects.filter(seller=user)
    active = []
    sold = []
    if request.method == "POST":
        # Close listing
        listing_id = request.POST.get("listing_id")
        item = Listing.objects.get(id=listing_id)
        seller = item.seller
        winner = bidCheck(listing_id)[1]
        if winner:
            cost = bidCheck(listing_id)[0]
            won = Winners(
                owner=seller,
                item=Listing(id=listing_id),
                winner=winner,
                cost=cost
            )
            item.sold = True
            won.save()
            item.save()
            messages.success(request,
                f"Congratulations! Your auction sold for ${cost} to {winner}!"
                )
            watchlist = Watchlist.objects.filter(item=Listing(id=item.id))
            for row in watchlist:
                row.delete()
            #watchlist.delete()
        else:
            messages.info(request,
                f"Your auction for {item.title} did not receive any bids."
                )
            item.delete()
        return HttpResponseRedirect(reverse("mylistings"))
    else:
        # Displays user's selling list
        for item in items:
            if item.sold == False:
                active.append(item)
            else:
                sold.append(item)
        active = bidUpdate(active)
        sold = bidUpdate(sold)
        data = {
            "Active Listings": active,
            "Sold": sold
        }
        return render(request, "auctions/mylistings.html", {
            "data": data
        })


# Allows user to create a new listing
@login_required(login_url='/login')
def new(request):
    if request.method == "POST":
        form = NewListForm(request.POST)
        if form.is_valid():
            user = request.user.id
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            start_bid = form.cleaned_data["start_bid"]
            category = request.POST.get("category")
            image = form.cleaned_data["image"]
            if not image:
                image="https://us.123rf.com/450wm/pavelstasevich/pavelstasevich1811/pavelstasevich181101028/112815904-no-image-available-icon-flat-vector-illustration.jpg?ver=6"
                
            new_listing = Listing(
                seller=User(id=user),
                title=title,
                description=description,
                start_bid=start_bid,
                image=image,
                category=category
                )
            new_listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = NewListForm()
        return render(request, "auctions/new.html", {
            "form": form,
            "categories": CATEGORIES
        })    


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Displays user's watchlist and handles adding/ removing behaviour
@login_required(login_url='/login')
def watchlist(request):
    user = request.user.id
    if request.method == "POST":
    # determine whether user wants to add or remove from watchlist
        listing_id = request.POST.get("listing_id")
        remove = request.POST.get("remove")
        watchlist = Watchlist(
            user=User(id=user), item=Listing(id=listing_id))
        if remove:
            watchlist = Watchlist.objects.filter(
                user=User(id=user), item=Listing(id=listing_id))
            watchlist.delete()
        else:
            watchlist.save()
        # return user to page they were on
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
    # display user's watchlist
        watchlist = Watchlist.objects.filter(user=user)
        watching_lst = []
        for items in watchlist:
            watching_lst.append(items.item)
        lst = bidUpdate(watching_lst)
        return render(request, "auctions/watchlist.html", {
            "watchlist": lst
        })