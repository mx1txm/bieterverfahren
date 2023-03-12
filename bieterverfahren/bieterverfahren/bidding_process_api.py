from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Seller, Property, BiddingProcess
from .serializers import BiddingProcessSerializer

#  the view uses the create_bidding_process function to handle the POST request with the required
#  information for creating a bidding process. The view checks if the seller and property with the
#  given IDs exist and returns an error response if not. If the seller and property exist, the view
#  creates a new BiddingProcess object with the given information, saves it to the database,
#  and returns the serialized data of the created object.


@api_view(['POST'])
def create_bidding_process(request):
    seller_id = request.data.get('seller_id')
    property_id = request.data.get('property_id')
    start_datetime = request.data.get('start_datetime')
    end_datetime = request.data.get('end_datetime')
    starting_price = request.data.get('starting_price')

    seller = Seller.objects.filter(id=seller_id).first()
    if not seller:
        return Response({'error': 'Seller not found'}, status=status.HTTP_400_BAD_REQUEST)

    property = Property.objects.filter(id=property_id).first()
    if not property:
        return Response({'error': 'Property not found'}, status=status.HTTP_400_BAD_REQUEST)

    bidding_process = BiddingProcess(
        seller=seller,
        property=property,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        starting_price=starting_price
    )
    bidding_process.save()

    serializer = BiddingProcessSerializer(bidding_process)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
