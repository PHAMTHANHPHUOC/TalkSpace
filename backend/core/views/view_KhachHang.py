from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from ..serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models.KhachHang import KhachHang
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.conf import settings
import uuid
from core.serializers import KhachHangSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import logging
logger = logging.getLogger(__name__)
# Custom exception handler để trả về thông báo tuỳ chỉnh khi chưa đăng nhập
# Để sử dụng, thêm vào settings.py:
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.TokenAuthentication',
#     ],
#     'EXCEPTION_HANDLER': 'core.views.custom_exception_handler',
# }

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def thong_tin(request):
    """
    Alternative: Trả về thông tin User thay vì KhachHang
    """
    try:
        user = request.user
        
        if not user or user.is_anonymous:
            return Response({
                'status': False,
                'message': "User chưa được xác thực"
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Sử dụng UserSerializer cho Django User
        serializer = UserSerializer(user)
        return Response({
            'status': True,
            'data': serializer.data
        })
        
    except Exception as e:
        return Response({
            'status': False,
            'message': f"Đã có lỗi xảy ra: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
def home(request):
    return render(request,'core/home.html')

@api_view(['GET'])
def kich_hoat_tai_khoan(request, hash_active):
    try:
        tai_khoan = KhachHang.objects.filter(hash_active=hash_active, is_active=0).first()
        if tai_khoan:
            tai_khoan.is_active = 1
            # tai_khoan.hash_active = None
            tai_khoan.save()
            return Response({
                'status': True,
                'message': "Bạn đã kích hoạt tài khoản thành công!"
            })
        else:
            return Response({
                'status': False,
                'message': "Tài khoản bạn đã được kích hoạt hoặc không tồn tại!"
            })
    except Exception as e:
        return Response({
            'status': False,
            'message': "Đã có lỗi xảy ra!"
        })


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = KhachHang.objects.get(email=email)
        if user.check_password(password):
            if not user.is_active:
                return Response({
                    'message': 'Tài khoản của bạn chưa được kích hoạt!',
                    'status': 2
                })
            elif getattr(user, 'is_block', False):
                return Response({
                    'message': 'Tài khoản của bạn đã bị khóa!',
                    'status': 0
                })
            else:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'message': 'Đã đăng nhập thành công!',
                    'status': 1,
                    'chia_khoa': token.key,
                    'ten_kh': user.ho_va_ten
                })
        else:
            return Response({
                'message': 'Tài khoản hoặc mật khẩu không đúng!',
                'status': 0
            }, status=status.HTTP_401_UNAUTHORIZED)
    except KhachHang.DoesNotExist:
        return Response({
            'message': 'Tài khoản hoặc mật khẩu không đúng!',
            'status': 0
        }, status=status.HTTP_401_UNAUTHORIZED)
@api_view(['POST'])
def signup(request):
    try:
        tai_khoan = KhachHang.objects.create(
            email=request.data['email'],
            so_dien_thoai=request.data['so_dien_thoai'],
            ho_va_ten=request.data['ho_va_ten'],
            password=make_password(request.data['password']),  
            hash_active=str(uuid.uuid4()), 
            hash_reset=str(uuid.uuid4()), 
        )
         # Gửi email kích hoạt
        subject = "Mời bạn kiểm tra email"
        to_email = tai_khoan.email
        # Render giao diện email
        html_content = render_to_string(
            'email/kich_hoat_tai_khoan.html',
            {
                'name': tai_khoan.ho_va_ten,
                'hash_active': tai_khoan.hash_active,  # hoặc 'hash_active': tai_khoan.hash_active nếu bạn muốn bảo mật hơn
            }
        )
        email = EmailMessage(subject, html_content, to=[to_email])
        email.content_subtype = "html"
        email.send()
        return Response({
                'status': True,
                'message': "Đăng Kí Thành Công - Mời Bạn Check Mail Để Kích Hoạt Tài Khoản!"
            })
    except Exception as e:
        print("ERROR:", e) 
        return Response({
            'status': False,
            'message': "Đã có lỗi xảy ra!"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
def quen_mat_khau(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        Khach_Hang = KhachHang.objects.filter(email=email).first()
        if Khach_Hang:
            subject = "Mời bạn kiểm tra email"
            html_content = render_to_string(
            'email/lay_lai_mat_khau.html',
            {
                'email': Khach_Hang,
                'hash_reset': Khach_Hang.hash_reset,  # hoặc 'hash_active': tai_khoan.hash_active nếu bạn muốn bảo mật hơn
            }
            )
            print('Hash reset:', Khach_Hang.hash_reset)
            email = EmailMessage(subject, html_content, to=[Khach_Hang.email])
            email.content_subtype = "html"
            email.send()

        return JsonResponse({
            'status': True,
            'message': "Kiểm tra email của bạn !!!"
        })
    except Exception as e:
        print("[Lỗi gửi email]", e) 
        return JsonResponse({
            'status': False,
            'message': "Đã có lỗi xảy ra!"
        })

@csrf_exempt
@api_view(['POST'])
def actionLaylaiMK(request, hash_reset):
    try:
        data = json.loads(request.body)
        password = data.get('password', '').strip()

        khach_hang = KhachHang.objects.filter(hash_reset=hash_reset).first()
        if khach_hang:
            khach_hang.password = make_password(password)  # bcrypt hóa password
            khach_hang.hash_reset = None
            khach_hang.save()

            return JsonResponse({
                'status': True,
                'message': "Mật khẩu đã được thay đổi"
            })

        return JsonResponse({
            'status': False,
            'message': "Đã có lỗi xảy ra!"
        })
    except Exception as e:
        return JsonResponse({
            'status': False,
            'message': "Lỗi máy chủ!"
        })


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def check_login(request):
    user = request.user
    if user and user.is_authenticated:
        return Response({
            'status': True,
            'message': 'Đã được đăng nhập',
            'user': getattr(user, 'ho_va_ten', )
        })
    else:
        return Response({
            'status': False,
            'message': 'Mời bạn đăng nhập'
        })

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        # Xóa token hiện tại
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
            return JsonResponse({'status': True, 'message': 'Bạn đã đăng xuất thành công!'}, status=200)
        else:
            return JsonResponse({'status': False, 'message': 'Không tìm thấy token!'}, status=400)
    except Exception as e:
        return JsonResponse({'status': False, 'message': f'Đăng xuất thất bại: {str(e)}'}, status=400)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_all(request):
    try:
        # Xóa tất cả token của user
        Token.objects.filter(user=request.user).delete()
        return JsonResponse({'status': True, 'message': 'Bạn đã đăng xuất tất cả thành công!'}, status=200)
    except Exception as e:
        return JsonResponse({'status': False, 'message': f'Đăng xuất tất cả thất bại: {str(e)}'}, status=400)











