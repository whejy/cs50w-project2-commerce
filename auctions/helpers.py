from .models import Listing, Bids


# Determine current highest bid and bidder for a listing
def bidCheck(listing_id):
    try:
        current_bid = None
        start_bid = Listing.objects.get(id=listing_id).start_bid
        bids = Bids.objects.filter(item=Listing(id=listing_id))
        highest_bid = bids.order_by('-bid').first()
        if highest_bid:
            current_bid = highest_bid.bid    
        else:
            current_bid = start_bid
        return current_bid, highest_bid.user
    # Catch for accessing invalid Listing via URL bar
    except Listing.DoesNotExist:
        return None, None
    # If no bid has been made, return the starting bid only
    except AttributeError:
        return current_bid, None


# Updates "current bid" for listings
def bidUpdate(items):
    lst=[]
    for item in items:
        current_bid = bidCheck(item.id)[0]
        product = Listing.objects.get(id=item.id)
        product.start_bid = current_bid
        lst.append(product) 
    return lst


# Takes in a list of values and returns only unique values
def unique(list1):
    list_set = set(list1)
    unique_list = (list(list_set))
    return unique_list