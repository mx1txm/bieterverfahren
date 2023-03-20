from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import BiddingProcess, Bid, Property
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.mail import send_mail


def landingpage(request):
    properties = Property.objects.all()
    context = {
        'property_list': properties,
    }
    return render(request, 'landingpage.html', context)


def send_invitation_email(bidding_process, recipient_email):
    subject = 'Invitation to participate in a bidding process'
    message = f'You have been invited to participate in the bidding process for {bidding_process.property}. The bidding process starts at {bidding_process.start_date} and ends at {bidding_process.end_date}. Please follow this link to place your bid: <link to your bidding page>'
    from_email = 'your-email@example.com'

    send_mail(subject, message, from_email, [recipient_email], fail_silently=False)


def bidding_process_detail(request, bidding_process_id):
    bidding_process = get_object_or_404(BiddingProcess, id=bidding_process_id)
    property = bidding_process.property
    bids = Bid.objects.filter(bidding_process=bidding_process).order_by('-amount')

    if request.method == 'POST':
        if bidding_process.is_closed():
            messages.error(request, _('The bidding process is closed. You cannot place a bid.'))
        else:
            bid_amount = request.POST.get('bid_amount')
            bidder_name = request.POST.get('bidder_name')
            if not bid_amount or not bidder_name:
                messages.error(request, _('Please enter a bid amount and a bidder name.'))
            else:
                try:
                    bid_amount = float(bid_amount)
                except ValueError:
                    messages.error(request, _('The bid amount must be a number.'))
                else:
                    bid = Bid.objects.create(
                        bidding_process=bidding_process,
                        bidder_name=bidder_name,
                        amount=bid_amount
                    )
                    messages.success(request, _('Your bid has been placed.'))

    return render(request, 'bidding_process_detail.html', {
        'property': property,
        'bidding_process': bidding_process,
        'bids': bids,
    })


@login_required
def bidders_list(request, property_id):
    property = Property.objects.get(id=property_id)

    # Check if the current user is the seller of the property
    if request.user != property.seller:
       return render(request, 'permission_denied.html')

    # Get all the bids for the property
    bids = Bid.objects.filter(bidding_process__property=property).order_by('-amount')

    return render(request, 'bidders_list.html', {
        'property': property,
        'bids': bids,
    })