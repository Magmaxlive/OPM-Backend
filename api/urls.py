from django.urls import path
from .views import *

urlpatterns = [
    path('blogs/',Blogs_view.as_view(),name='blog'),
    path('blogs/<str:slug>/',Blogs_detail_view.as_view(),name='blog'),
    path('enquiry/',Enquiry_form_view.as_view(),name='enquiry'),
    path('subscribe/',Subscriber_form_view.as_view(),name='subscribe'),
    path('rental_appraisal/',Rental_form_view.as_view(),name='rental_appraisal')
]