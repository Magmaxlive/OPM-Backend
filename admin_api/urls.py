from django.urls import path
from .views import *

urlpatterns = [
    path('blogs/',Blogs_view.as_view(),name='blog'),
    path('blogs/<int:pk>/',Blogs_detail_view.as_view(),name='blog'),
    path('enquiries/',Enquiries_view.as_view(),name='enquiry'),
    path('enquiries/<int:pk>/',Enquiries_detail_view.as_view(),name='enquiry'),

    # path('subscribe/',Subscriber_form_view.as_view(),name='subscribe'),
    # path('rental_appraisal/',Rental_form_view.as_view(),name='rental_appraisal')


    # auth

    path('auth/login/',login_view,name='login'),
    path('auth/logout/',logout_view,name='logout'),
    path('auth/profile/',Profile_view,name='profile'),
    path('auth/refresh/', refresh_view, name='refresh'),
    path('auth/change-password/', Change_password_view),
]