from rest_framework import serializers
from django.contrib.auth.models import User
from .models.CapDo import CapDo
from .models.ChuDe import ChuDe
from .models.NgonNgu import NgonNgu

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

class CapDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapDo
        fields = ['id', 'ten_cap_do', 'mo_ta']

class NgonNguSerializer(serializers.ModelSerializer):
    class Meta:
        model = NgonNgu
        fields = ['id', 'ten_ngon_ngu']

class ChuDeSerializer(serializers.ModelSerializer):
    ngon_ngu = NgonNguSerializer(read_only=True)
    
    class Meta:
        model = ChuDe
        fields = ['id', 'ten_chu_de', 'ngon_ngu']

class BaiHocSerializer(serializers.ModelSerializer):
    chu_de = ChuDeSerializer(read_only=True)
    ngon_ngu = NgonNguSerializer(read_only=True)
    nguoi_tao = KhachHangSerializer(read_only=True)
    
    class Meta:
        # model = BaiHoc
        fields = ['id', 'ten_bai_hoc', 'chu_de', 'noi_dung', 'ngon_ngu', 'ngay_tao', 'nguoi_tao']
        read_only_fields = ['ngay_tao', 'nguoi_tao']
