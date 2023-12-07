from django.urls import path
from .views import (
    signup, 
    login_user,  
    logout_user,
    get_all_users,
    get_all_photographers,
    get_all_clients,
    get_all_staff,
    staff_detail,
    photographer_detail,
    client_detail,  
    booking_list,
    booking_detail,
    booking_history_list,
    booking_history_detail,
    work_history_list,
    work_history_detail
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    # Authentication endpoints
    path('signup/', signup, name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    
    # JWT token authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verify/', TokenVerifyView.as_view(), name="token_verify"),

     # User-related endpoints
    path('users/', get_all_users, name='get_all_users'),
    path('users/staff/<int:id>/', staff_detail, name='staff_detail'),
    path('users/photographer/<int:id>/', photographer_detail, name='photographer_detail'),
    path('users/client/<int:id>/', client_detail, name='client_detail'),

    # get specific User-related endpoints
    path('photographers/', get_all_photographers, name='get_all_photographers'),
    path('clients/', get_all_clients, name='get_all_clients'),
    path('staff/', get_all_staff, name='get_all_staff'),

    # Booking-related endpoints
    path('bookings/', booking_list, name='booking_list'),
    path('bookings/<int:id>/', booking_detail, name='booking_detail'),

    # Booking history endpoints
    path('booking-history/', booking_history_list, name='booking_history_list'),
    path('booking-history/<int:id>/', booking_history_detail, name='booking_history_detail'),

    # Work history endpoints
    path('work-history/', work_history_list, name='work_history_list'),
    path('work-history/<int:id>/', work_history_detail, name='work_history_detail'),
]
