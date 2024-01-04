from rest_framework import serializers
from .models import (
    User, 
    Staff, 
    Photographer, 
    Client, 
    Bookings, 
    BookingHistory, 
    JobPost, 
    JobApplication, 
    WorkHistory, 
    Notification,
    Profile, 
    ProfileSwitch
)
from rest_framework.authtoken.models import Token

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ProfileSwitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileSwitch
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

    class Meta:
        model = User
        fields = '__all__'

   
    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()
        if email_exists:
            raise serializers.ValidationError("Email has already been used")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user=super().create(validated_data)
        
        user.set_password(password)
        user.save()

        Token.objects.create(user=user)
        return user
