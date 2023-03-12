from django.contrib import admin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from .models import Seller, Property, BiddingProcess, Bid


class PropertyInline(admin.TabularInline):
    model = Property
    extra = 1


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    inlines = [PropertyInline]


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('address', 'seller')
    list_filter = ('seller',)


@admin.register(BiddingProcess)
class BiddingProcessAdmin(admin.ModelAdmin):
    list_display = ('property', 'start_time', 'end_time', 'starting_price', 'minimum_increment')
    list_filter = ('property__seller', 'start_time', 'end_time')
    readonly_fields = ('current_highest_bid',)
    fieldsets = (
        (None, {
            'fields': ('property', 'start_time', 'end_time', 'starting_price', 'minimum_increment')
        }),
        (_('Extension Time'), {
            'fields': ('duration_extension_time',),
            'description': _('Duration to extend the bidding process when a bid is placed less than 10 minutes before the end.')
        }),
        (_('Bidders'), {
            'fields': ('invited_bidders',),
            'description': _('Bidders who have been invited to the bidding process.')
        }),
        (_('Current Bids'), {
            'fields': ('current_highest_bid',),
            'description': _('The current highest bid for this bidding process.')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.save()
            self.invite_bidders(request, obj)
        else:
            obj.save()

    def invite_bidders(self, request, bidding_process):
        subject = _('Invitation to bid')
        from_email = 'example@example.com'
        template_name = 'email/bidding_process_invitation.html'

        for bidder_email in bidding_process.invited_bidders.split(','):
            bidder_email = bidder_email.strip()
            if bidder_email:
                context = {
                    'seller_name': bidding_process.property.seller.name,
                    'property_address': bidding_process.property.address,
                    'bidding_process_start_time': bidding_process.start_time,
                    'bidding_process_end_time': bidding_process.end_time,
                    'bidding_process_starting_price': bidding_process.starting_price,
                    'bidding_process_minimum_increment': bidding_process.minimum_increment,
                }
                html_message = render_to_string(template_name, context)
                plain_message = strip_tags(html_message)
                send_mail(subject, plain_message, from_email, [bidder_email], html_message=html_message)

    def current_highest_bid(self, obj):
        highest_bid = obj.current_highest_bid()
        if highest_bid:
            return f'{highest_bid.bidder_name}: {highest_bid.amount}'
        return None

    current_highest_bid.short_description = _('Current highest bid')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields['invited_bidders'].help_text = _('Enter a comma-separated list of email addresses.')
        return form

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
