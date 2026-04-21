from rest_framework import serializers
from .models import Blog,Enquiry_form,Subscribers_Form,Rental_form


class Blog_serializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'

    def get_cover_image(self, obj):
        if not obj.cover_image:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.cover_image.url)
        return obj.cover_image.url
    
class Blog_serializer_admin(serializers.ModelSerializer):
    cover_image = serializers.ImageField(required=False)

    class Meta:
        model = Blog
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.cover_image:
            request = self.context.get('request')
            rep['cover_image'] = request.build_absolute_uri(instance.cover_image.url) if request else instance.cover_image.url
        return rep
    
class Enquiry_serializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry_form
        fields = '__all__'


class Subscriber_serializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribers_Form
        fields = '__all__'
        

class Rental_serializer(serializers.ModelSerializer):
    class Meta:
        model = Rental_form
        fields = "__all__"
