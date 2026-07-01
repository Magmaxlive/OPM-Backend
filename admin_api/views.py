from django.shortcuts import render
from rest_framework import generics
from api.models import Blog, Enquiry_form, Subscribers_Form, Rental_form
from api.serializers import Blog_serializer, Enquiry_serializer,Blog_serializer_admin, Subscriber_serializer, Rental_serializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.contrib.auth import update_session_auth_hash
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import ValidationError

DOMAIN = ".oaksproperty.co.nz"


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid credentials Provided'}, status=401)

    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)

    response = Response({'message': 'Login successful'})
    response.set_cookie(key='access_token', value=access, httponly=True, secure=True, samesite='Lax', max_age=60*60, path='/',domain=DOMAIN,)
    response.set_cookie(key='refresh_token', value=str(refresh), httponly=True, secure=True, samesite='Lax', max_age=60*60*24*7, path='/',domain=DOMAIN,)
    return response


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_view(request):
    refresh_token = request.COOKIES.get('refresh_token')
    if not refresh_token:
        return Response({'error': 'No refresh token'}, status=401)

    serializer = TokenRefreshSerializer(data={'refresh': refresh_token})
    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError:
        return Response({'error': 'Invalid refresh token'}, status=401)

    response = Response({'message': 'Token refreshed'})
    response.set_cookie(key='access_token', value=serializer.validated_data['access'], httponly=True, secure=True, samesite='Lax', max_age=60*60, path='/',domain=DOMAIN,)
    if 'refresh' in serializer.validated_data:
        response.set_cookie(key='refresh_token', value=serializer.validated_data['refresh'], httponly=True, secure=True, samesite='Lax', max_age=60*60*24*7, path='/',domain=DOMAIN,)
    return response


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    refresh_token = request.COOKIES.get('refresh_token')
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            pass  # Token invalid, already blacklisted, or DB error — ignore

    response = Response({'message': 'Logged Out'})

    response.delete_cookie(
        key='access_token', 
        path='/',
        secure=True,
        samesite='Lax',
        domain=DOMAIN
    )

    response.delete_cookie(
        key='refresh_token', 
        path='/',
        secure=True,
        samesite='Lax',
        domain=DOMAIN
    )
    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Profile_view(request):
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Change_password_view(request):
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    if not current_password or not new_password or not confirm_password:
        return Response({'error': 'All Fields are required'}, status=400)
    if not request.user.check_password(current_password):
        return Response({'error': 'Current password is incorrect'}, status=400)
    if new_password != confirm_password:
        return Response({'error': 'New Passwords do not match'}, status=400)
    if len(new_password) < 8:
        return Response({'error': 'Password must be at least 8 characters'}, status=400)

    request.user.set_password(new_password)
    request.user.save()
    update_session_auth_hash(request, request.user)
    return Response({'message': 'Password Changed Successfully'})


class Pagination(PageNumberPagination):
    page_size = 10

class Blog_Pagination(PageNumberPagination):
    page_size = 6


class Enquiries_view(generics.ListAPIView):
    serializer_class = Enquiry_serializer
    queryset = Enquiry_form.objects.all().order_by('-id')
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['full_name', 'email', 'subject']


class Enquiries_detail_view(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = Enquiry_serializer
    queryset = Enquiry_form.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class Rental_view(generics.ListAPIView):
    serializer_class = Rental_serializer
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'property_type']
    search_fields = ['first_name', 'last_name', 'email', 'address']
    queryset = Rental_form.objects.all().order_by('-id')


class Rental_detail_view(generics.RetrieveUpdateAPIView):
    serializer_class = Rental_serializer
    permission_classes = [IsAuthenticated]
    queryset = Rental_form.objects.all()
    lookup_field = 'pk'


class Blogs_view(generics.ListCreateAPIView):
    serializer_class = Blog_serializer_admin
    permission_classes = [IsAuthenticated]
    pagination_class = Blog_Pagination

    def get_queryset(self):
        qs = Blog.objects.all().order_by('-id')
        status = self.request.query_params.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_serializer_context(self):
        return {'request': self.request, 'format': self.format_kwarg, 'view': self}

class Blogs_detail_view(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = Blog_serializer_admin
    queryset = Blog.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}
    

class Subscribers_view(generics.ListAPIView):
    serializer_class = Subscriber_serializer
    queryset = Subscribers_Form.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['email']


class Subscriber_detail_view(generics.RetrieveDestroyAPIView):
    serializer_class = Subscriber_serializer
    queryset = Subscribers_Form.objects.all()
    lookup_field = 'pk'
