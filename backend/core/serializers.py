from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password','email']
from rest_framework import serializers
from .models import KhachHang

class KhachHangSerializer(serializers.ModelSerializer):
    class Meta:
        model = KhachHang
        fields = ['id', 'username', 'password', 'email', 'hash_active']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = KhachHang(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# class serializers(serializers.ModelSerializer):
#     class Meta(object):
#         model = User
#         fields = ['id','username','password','email']