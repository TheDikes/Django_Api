# utils.py
import jwt
from datetime import datetime, timedelta
from django.urls import reverse
from django.core.mail import send_mail
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings



# CustomToken 
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            refresh = response.data.get('refresh')
            access = response.data.get('access')
            if refresh and access:
                response.set_cookie('refresh_token', refresh, httponly=True)
                response.data = {'access_token': access}
        return response



def send_verification_email(email, selected_profile, token):
    """Construct the verification URL and send it in the email
     Your email sending logic using Django's send_mail() function here
     Include the verification URL in the email body 
    """
     # Construct the verification URL using reverse()
    verification_url = reverse('confirm_switch_profile', args=[selected_profile, token])
    
    # Compose the email subject and body
    subject = 'Confirmation for Profile Switch'
    message = f'Hi there!\n\nPlease confirm your switch to the {selected_profile} profile by clicking the following link:\n\n{verification_url}\n\nThis link will expire after a certain duration for security purposes. If you did not initiate this request, please ignore this email.\n\nBest regards,\nYourAppName Team'

    # Send the email using Django's send_mail() function
    send_mail(
        subject,
        message,
        'from@example.com',  # Sender's email address
        [email],  # Recipient's email address, can be a list for multiple recipients
        fail_silently=False,  # Set it to True to suppress errors when sending fails
    )



def generate_verification_token(user, selected_profile):
    payload = {
        'user_id': user.id,
        'selected_profile': selected_profile,
        'exp': datetime.utcnow() + timedelta(hours=24)  # Token expiration time
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')


def verify_verification_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload  # Return the payload if the token is valid
    except jwt.ExpiredSignatureError:
        return 'Token expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'