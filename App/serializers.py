from rest_framework import serializers
from .models import Turf ,Booking


class TurfSerializer(serializers.ModelSerializer):

    class Meta:
        model = Turf
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = '__all__'