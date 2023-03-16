from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _


class Seller(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Property(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='properties')
    address = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to='property_photos')

    def __str__(self):
        return self.address


class BiddingProcess(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='bidding_process')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_increment = models.DecimalField(max_digits=10, decimal_places=2)
    duration_extension_time = models.DurationField(default='0h:10m', help_text=_('Duration extends 10 minutes'))
    # Duration to extend the bidding process when a bid is placed less than 10 minutes before the end.
    invited_bidders = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Bidding process for {self.property}'

    def current_highest_bid(self):
        return self.bids.order_by('-amount').first()

    def current_highest_bidder(self):
        highest_bid = self.current_highest_bid()
        if highest_bid:
            return highest_bid.bidder
        return None


class Bid(models.Model):
    bidding_process = models.ForeignKey(BiddingProcess, on_delete=models.CASCADE, related_name='bids')
    bidder_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def pseudonymized_bid(self):
        return f'{self.bidder_name[:6]}: {self.amount}'

    def save(self, *args, **kwargs):
        if not self.pk:
            # New bid is being created
            bidding_process = self.bidding_process
            time_left = bidding_process.end_time - datetime.datetime.now(datetime.timezone.utc)
            if time_left.total_seconds() < 600:
                # Bidding process is ending in less than 10 minutes, so extend the duration by 10 minutes
                bidding_process.end_time += datetime.timedelta(minutes=10)
                bidding_process.save()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-amount', 'created_at']

# Now, when a bid is placed less than 10 minutes before the end of the bidding process, the bidding process's end time will be automatically extended by 10 minutes.
# To update the page and bids automatically using htmx or websockets, we can use JavaScript to periodically send requests to the server to check for updates. Here's an example using htmx:
# pip install htmx

#Seller:
#name: The name of the seller.
#email: The email address of the seller.
#phone: The phone number of the seller.

#Property:
#seller: The seller who owns the property.
#address: The address of the property.
#description: A description of the property.
#photo: A photo of the property.

#BiddingProcess:
#property: The property being auctioned.
#start_time: The start time of the bidding process.
#end_time: The end time of the bidding process.
#starting_price: The starting price of the bidding process.
#minimum_increment: The minimum increment for each bid.
#duration_extension_time: The duration to extend the bidding process when a bid is placed less than 10 minutes before the end.

#Bid:
#bidding_process: The bidding process the bid belongs to.
#bidder_name: The name of the bidder (pseudonymized in the front-end).
#amount: The amount of the bid.
#created_at: The time the bid was placed.


