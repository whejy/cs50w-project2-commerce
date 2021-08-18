from django.contrib import admin
from .models import User, Listing, Bids, Comments, Watchlist, Winners

# Register your models here.

class BidsAdmin(admin.ModelAdmin):
    list_display=('user', 'get_item', 'bid')

    def get_item(self, obj):
        return obj.item.title
    get_item.admin_order_field = 'item'
    get_item.short_description = "Item"


class ListingAdmin(admin.ModelAdmin):
    list_display=('seller', 'item_name', 'start_bid', 'category', 'sold', 'date_name')

    def date_name(self, obj):
        return obj.date
    date_name.short_description = "Date Created"

    def item_name(self, obj):
        return obj.title
    item_name.short_description = "Item"


class WinnersAdmin(admin.ModelAdmin):
    list_display=('owner', 'winner', 'get_item', 'cost')

    def get_item(self, obj):
        return obj.item.title
    get_item.admin_order_field = 'item'
    get_item.short_description = "Item"


admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bids, BidsAdmin)
admin.site.register(Comments)
admin.site.register(Watchlist)
admin.site.register(Winners, WinnersAdmin)
