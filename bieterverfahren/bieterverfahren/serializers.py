from rest_framework import serializers
from .models import BiddingProcess

class BiddingProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiddingProcess
        fields = '__all__'
