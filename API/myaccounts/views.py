from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import User, Photographer, Client, Staff, Bookings, BookingHistory, JobPost, JobApplication, WorkHistory
from .serializers import (
    UserSerializer, 
    PhotographerSerializer, 
    ClientSerializer, 
    StaffSerializer,
    BookingSerializer, 
    BookingHistorySerializer, 
    JobPostSerializer,
    JobApplicationSerializer,
    WorkHistorySerializer
)
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .utils import generate_verification_token, send_verification_email, verify_verification_token 
    

# User Registration
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow unauthenticated access
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user_type = request.data.get('user_type')  
        if user_type not in [1, 2, 3]:  # Checking if user_type is valid
            return Response({'message': 'Invalid user type'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save(user_type=user_type)

        # Generate JWT tokens upon successful registration
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# User Login
@api_view(['POST'])
@permission_classes([AllowAny]) 
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if email and password:
        user = authenticate(request, email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'message': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)



# User Logout
@api_view(['POST'])
def logout_user(request):
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()  # Blacklist or invalidate the token
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Invalid token or logout failed'}, status=status.HTTP_400_BAD_REQUEST)



# Retrieve all users
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def get_all_photographers(request):
    photographers = Photographer.objects.all()
    serializer = PhotographerSerializer(photographers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def get_all_clients(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def get_all_staff(request):
    staff = Staff.objects.all()
    serializer = StaffSerializer(staff, many=True)
    return Response(serializer.data)

# Create Bookings
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def booking_list(request):
    if request.method == 'GET':
        bookings = Bookings.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=request.user)  # Assuming the client is creating the booking
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create Booking history
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def booking_history_list(request):
    if request.method == 'GET':
        booking_history = BookingHistory.objects.all()
        serializer = BookingHistorySerializer(booking_history, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookingHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=request.user)  # Assuming the client is creating the booking history
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create Job Post
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def job_post_list(request):
    if request.method == 'GET':
        job_posts = JobPost.objects.all()
        serializer = JobPostSerializer(job_posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = JobPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=request.user.client_profile)  # Assuming the client is creating the job post
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Create Job Application
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_for_job(request, job_post_id):
    try:
        job_post = JobPost.objects.get(pk=job_post_id)
    except JobPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = JobApplicationSerializer(data=request.data)
    if serializer.is_valid():
        # Assuming you have access to the authenticated photographer and client
        photographer = request.user.photographer  # Get the authenticated photographer
        client = job_post.client  # Get the client who posted the job
        serializer.save(job_post=job_post, photographer=photographer, client=client)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create work history 
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def work_history_list(request):
    if request.method == 'GET':
        work_history = WorkHistory.objects.all()
        serializer = WorkHistorySerializer(work_history, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WorkHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(photographer=request.user)  # Assuming the photographer is creating the work history
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Retrieve, update, Delete Staff by ID
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def staff_detail(request, id):
    try:
        staff = User.objects.get(pk=id, user_type=1) # user_type 3 is for clients
    except User.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method =='GET':
        serializer = UserSerializer(staff)
        return Response(serializer.data)
    elif request.method =='PUT':
        serializer = UserSerializer(staff, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        staff.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# Retrieve, Update, Delete Photographer by ID
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def photographer_detail(request, id):
    try:
        photographer = User.objects.get(pk=id, user_type=2)  # user_type 2 is for photographers
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(photographer)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(photographer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        photographer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Retrieve, Update, Delete Client by ID
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def client_detail(request, id):
    try:
        client = User.objects.get(pk=id, user_type=3)  # user_type 3 is for clients
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(client)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Retrieve, Update, Delete Booking by ID
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def booking_detail(request, id):
    try:
        booking = Bookings.objects.get(pk=id)
    except Bookings.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookingSerializer(booking)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Retrieve, Update, Delete Booking history by ID
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def booking_history_detail(request, id):
    try:
        booking_history = BookingHistory.objects.get(pk=id)
    except BookingHistory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookingHistorySerializer(booking_history)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BookingHistorySerializer(booking_history, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        booking_history.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# Retrieve, Update, Delete Job Post by ID
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def job_post_detail(request, id):
    try:
        job_post = JobPost.objects.get(pk=id)
    except JobPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JobPostSerializer(job_post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = JobPostSerializer(job_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        job_post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def job_application_detail(request, application_id):
    try:
        job_application = JobApplication.objects.get(pk=application_id)
    except JobApplication.DoesNotExist:
        return Response({'message': 'Job application not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JobApplicationSerializer(job_application)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = JobApplicationSerializer(job_application, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        job_application.delete()
        return Response({'message': 'Job application deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# Retrieve, Update, Delete Work history by ID
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def work_history_detail(request, id):
    try:
        work_history = WorkHistory.objects.get(pk=id)
    except WorkHistory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WorkHistorySerializer(work_history)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = WorkHistorySerializer(work_history, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        work_history.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def switch_profile(request):
    if request.method == 'POST':
        selected_profile = request.data.get('selected_profile')
        entered_email = request.data.get('email')

        user = request.user
        if user.email != entered_email:
            return Response({'message': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            verification_token = generate_verification_token(user, selected_profile)
            send_verification_email(user.email, selected_profile, verification_token)
            return Response({'message': 'Verification email sent'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error_message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def confirm_switch_profile(request, selected_profile, token):
    verification_result = verify_verification_token(token)
    if isinstance(verification_result, dict) and verification_result['user_id'] == request.user.id:
        User = User.model()
        user = User.objects.get(id=request.user.id)
        
        """ Switch profile logic based on the selected_profile value """
        if selected_profile == 'client':
            user.is_client = True
            user.is_photographer = False
        elif selected_profile == 'photographer':
            user.is_client = False
            user.is_photographer = True
        else:
            return Response({'message': 'Invalid profile selection'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.save()
        return Response({'message': 'Profile switched successfully'}, status=status.HTTP_200_OK)
    
    return Response({'message': 'Invalid verification token'}, status=status.HTTP_400_BAD_REQUEST)
