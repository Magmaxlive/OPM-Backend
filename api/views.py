from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from .models import *
from rest_framework.pagination import PageNumberPagination


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


class Subscriber_form_view(generics.CreateAPIView):
    serializer_class = Subscriber_serializer
    queryset = Subscribers_Form.objects.all()


class Rental_form_view(generics.CreateAPIView):
    serializer_class = Rental_serializer
    queryset = Rental_form.objects.all()