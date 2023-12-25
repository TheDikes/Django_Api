from rest_framework import serializers
from .models import User, Staff, Photographer, Client, Bookings, BookingHistory, JobPost, JobApplication, WorkHistory
from rest_framework.authtoken.models import Token


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = '__all__'

class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'

class BookingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingHistory
        fields = '__all__'

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
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
    work_history = WorkHistorySerializer(many=True, required=False)

    class Meta:
        model = Photographer
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    bookings = BookingSerializer(many=True, required=False)
    booking_history = BookingHistorySerializer(many=True, required=False)

    class Meta:
        model = Client
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)
    staff = StaffSerializer(required=False)
    photographer = PhotographerSerializer(required=False)
    client = ClientSerializer(required=False)

    class Meta:
        model = User
        fields = '__all__'


        
    def create(self, validated_data):
        password = validated_data.pop("password")
        user=super().create(validated_data)
        
        user.set_password(password)
        user.save()

        Token.objects.create(user=user)
        return user