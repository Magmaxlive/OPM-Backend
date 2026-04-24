from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from .models import *
from rest_framework.pagination import PageNumberPagination
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


class BlogPagination(PageNumberPagination):
    page_size = 6

class Blogs_view(generics.ListAPIView):
    serializer_class = Blog_serializer
    pagination_class = BlogPagination

    def get_queryset(self):
        return Blog.objects.filter(status='published')

    def get_serializer_context(self):
        return {'request': self.request}


class Blogs_detail_view(generics.RetrieveAPIView):
    serializer_class = Blog_serializer
    lookup_field = 'slug'
    queryset = Blog.objects.all()


class Enquiry_form_view(generics.CreateAPIView):
    serializer_class = Enquiry_serializer
    queryset = Enquiry_form.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        self.send_enquiry_email(instance)
        
    def send_enquiry_email(self,instance):

        context = {
           'name' : instance.full_name,
           'email' : instance.email,
           'subject' : instance.subject,
           'phone' : instance.phone,
           'message' : instance.message 
        }

        html_content = render_to_string('emails/enquiry.html',context)
        text_context = f"New Enquiry from {instance.full_name} - {instance.email}"

        email = EmailMultiAlternatives(
            subject=f"New Enquiry from {instance.full_name}",
            body=text_context,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.RECIEVER_EMAIL],
            reply_to=[instance.email]
        )

        email.attach_alternative(html_content,"text/html")
        email.send(fail_silently=False)

class Subscriber_form_view(generics.CreateAPIView):
    serializer_class = Subscriber_serializer
    queryset = Subscribers_Form.objects.all()


class Rental_form_view(generics.CreateAPIView):
    serializer_class = Rental_serializer
    queryset = Rental_form.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        self.send_rental_email(instance)
        
    def send_rental_email(self,instance):

        context = {
           'first_name' : instance.first_name,
           'last_name' : instance.last_name,
           'email' : instance.email,
           'address' : instance.address,
           'phone' : instance.phone,
           'property_type' : instance.property_type,
           'current_status' : instance.current_status,
           'bedrooms' : instance.bedrooms,
           'bathrooms' : instance.bathrooms,
           'appraisal_date' : instance.appraisal_date,
           'note' : instance.note,
        }

        html_content = render_to_string('emails/rental.html',context)
        text_context = f"New Rental Appraisal from {instance.first_name} - {instance.email}"

        email = EmailMultiAlternatives(
            subject=f"New Rental Appraisal from {instance.first_name}",
            body=text_context,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.RECIEVER_EMAIL],
            reply_to=[instance.email]
        )

        email.attach_alternative(html_content,"text/html")
        email.send(fail_silently=False)