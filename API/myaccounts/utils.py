import jwt
from datetime import datetime, timedelta
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status


def send_verification_email(email, selected_profile, token):
    """Construct the verification URL and send it in the email
       Uses Django's send_mail() function, include the verification URL in the email body 
    """
    verification_url = reverse('confirm_switch_profile', args=[selected_profile, token])
    subject = 'Confirmation for Profile Switch'
    message = f'''Hi there!
    \n\nPlease confirm your switch to the {selected_profile} profile by clicking the following link:
    \n\n{verification_url}\n\nThis link will expire after a certain duration for security purposes. 
    If you did not initiate this request, please ignore this email.
    \n\nBest regards,\nPictoria Photography Team'''


    try:
        send_mail(
            subject,
            message,
            'from@example.com',  # Sender's email address
            [email],  # Recipient's email address, can be a list for multiple recipients
            fail_silently=False,  # Set it to True to suppress errors when sending fails
            )
        return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def generate_verification_token(user, selected_profile):
    payload = {
        'user_id': user.id,
        'selected_profile': selected_profile,
        'exp': datetime.utcnow() + timedelta(minutes=5)  # Token expiration time
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