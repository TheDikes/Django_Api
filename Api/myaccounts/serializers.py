from rest_framework import serializers
from .models import User, Staff, Photographer, Client, Bookings, BookingHistory, WorkHistory

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = '__all__'

class BookingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingHistory
        fields = '__all__'

class WorkHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkHistory
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class PhotographerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(required=False)
    photographer = PhotographerSerializer(required=False)
    client = ClientSerializer(required=False)
    bookings = BookingSerializer(many=True, required=False)
    booking_history = BookingHistorySerializer(many=True, required=False)
    work_history = WorkHistorySerializer(many=True, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'user_type',
            'staff', 'photographer', 'client',
            'bookings', 'booking_history', 'work_history'
        ]

    def update(self, instance, validated_data):
        user_type = instance.user_type

        # Extract specific user type related data and handle updates here if necessary

        return super().update(instance, validated_data)

