from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from core.models.HoSoHocTap import HoSoHocTap
from core.models.KhachHang import KhachHang
from core.models.NgonNgu import NgonNgu
from core.models.CapDo import CapDo
from core.models.ChuDe import ChuDe
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view


@csrf_exempt
@api_view(['POST'])
def create_HoSo(request):
        try:
            if not request.user.is_authenticated:
                return JsonResponse({'success': False, 'message': 'Bạn chưa đăng nhập.'}, status=401)

            data = json.loads(request.body)
            ho_ten = data.get('ho_ten')
            ngay_sinh = data.get('ngay_sinh')
            gioi_tinh = data.get('gioi_tinh', 'Khac')
            ngon_ngu_id = data.get('ngon_ngu')
            # trinh_do_id = data.get('trinh_do')

            khach_hang = request.user  # Lấy user hiện tại
            ngon_ngu = NgonNgu.objects.get(id=ngon_ngu_id) if ngon_ngu_id else None
            # trinh_do = CapDo.objects.get(id=trinh_do_id) if trinh_do_id else None

            # Tạo hồ sơ mới trực tiếp
            hoso = HoSoHocTap.objects.create(
                khach_hang=khach_hang,
                ho_ten=ho_ten,
                ngay_sinh=ngay_sinh,
                gioi_tinh=gioi_tinh,
                ngon_ngu_hoc=ngon_ngu,
                # trinh_do=trinh_do,
            )
            return JsonResponse({'success': True, 'message': 'Tạo hồ sơ học tập thành công.', 'id': hoso.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_GET
@api_view(['GET'])
@login_required
def data_HoSo(request):
    khach_hang = request.user
    data = HoSoHocTap.objects.filter(khach_hang_id=khach_hang.id).values(
        'id', 'ho_ten', 'ngay_sinh', 'gioi_tinh', 'khach_hang_id', 'ngon_ngu_hoc_id'
    )
    return JsonResponse({'data': list(data)})

@require_GET
def data_CapDo(request):
    data = list(CapDo.objects.all().values('id', 'ten_cap_do', 'mo_ta'))
    return JsonResponse({'data': data})

@require_GET
def data_NgonNgu(request):
    data = list(NgonNgu.objects.all().values('id', 'ten_ngon_ngu', 'ma_ngon_ngu'))
    return JsonResponse({'data': data})
@require_GET
def data_ChuDe(request):
    data = list(ChuDe.objects.all().values('id', 'ten_chu_de', 'ngon_ngu_id'))
    return JsonResponse({'data': data})

@require_GET
@api_view(['GET'])
@login_required
def get_user_language(request):
    """
    Lấy ngôn ngữ học của user hiện tại từ hồ sơ học tập
    """
    try:
        khach_hang = request.user
        hoso_id = request.GET.get('hoso_id')
        
        if hoso_id:
            # Lấy hồ sơ học tập theo hoso_id được chỉ định
            hoso = HoSoHocTap.objects.filter(khach_hang=khach_hang, id=hoso_id).first()
        else:
            # Lấy hồ sơ học tập đầu tiên của user nếu không có hoso_id
            hoso = HoSoHocTap.objects.filter(khach_hang=khach_hang).first()
        
        if hoso and hoso.ngon_ngu_hoc:
            return JsonResponse({
                'success': True,
                'language': {
                    'id': hoso.ngon_ngu_hoc.id,
                    'name': hoso.ngon_ngu_hoc.ten_ngon_ngu,
                    'code': hoso.ngon_ngu_hoc.ma_ngon_ngu,
                    'gtts_code': hoso.ngon_ngu_hoc.ma_ngon_ngu
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Không tìm thấy hồ sơ học tập hoặc ngôn ngữ học'
            }, status=404)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@api_view(['DELETE'])
@login_required
def delete_HoSo(request, id):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'Bạn chưa đăng nhập.'}, status=401)
        
        # Lấy hồ sơ học tập theo ID và khách hàng hiện tại
        hoso = HoSoHocTap.objects.filter(id=id, khach_hang=request.user).first()
        
        if not hoso:
            return JsonResponse({'success': False, 'message': 'Không tìm thấy hồ sơ học tập hoặc bạn không có quyền xóa.'}, status=404)
        
        # Xóa hồ sơ
        hoso.delete()
        
        return JsonResponse({'success': True, 'message': 'Xóa hồ sơ học tập thành công.'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Có lỗi xảy ra: {str(e)}'}, status=500)
