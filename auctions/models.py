from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="listings"
        )
    title = models.CharField(max_length=64)
    description = models.TextField()
    start_bid = models.DecimalField(
        max_digits=8,
        decimal_places=2
        )
    image = models.URLField(
        null=True,
        default="https://us.123rf.com/450wm/pavelstasevich/pavelstasevich1811/pavelstasevich181101028/112815904-no-image-available-icon-flat-vector-illustration.jpg?ver=6"
        )
    category = models.CharField(
        max_length=64,
        null=True,
        blank=True
        )
    sold = models.BooleanField(
        default=False
        )
    
    def __str__(self):
        return f"{self.id}: {self.title}, {self.description}, {self.start_bid}, {self.image}, {self.category}"


class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        null=True,
        blank=True
        )

    def __str__(self):
        return f"{self.user}: {self.item} {self.bid}" 

    class Meta:
        verbose_name_plural = "bids"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"User: {self.user.id} Item: {self.item}"

    class Meta:
        verbose_name_plural = "watchlist"


class Winners(models.Model):
    owner = models.CharField(max_length=64, null=True, blank=True)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    winner = models.CharField(max_length=64, null=True, blank=True)
    cost = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        null=True,
        blank=True
    )
    notified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "winners"


class Comments(models.Model):
    user = models.CharField(max_length=64)
    listing_id = models.IntegerField()
    comment = models.TextField()

    class Meta:
        verbose_name_plural = "comments"