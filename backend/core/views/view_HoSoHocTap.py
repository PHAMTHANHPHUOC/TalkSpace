from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from core.models.HoSoHocTap import HoSoHocTap
from core.models.KhachHang import KhachHang
from core.models.NgonNgu import NgonNgu
from core.models.CapDo import CapDo
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
            trinh_do_id = data.get('trinh_do')

            khach_hang = request.user  # Lấy user hiện tại
            ngon_ngu = NgonNgu.objects.get(id=ngon_ngu_id) if ngon_ngu_id else None
            trinh_do = CapDo.objects.get(id=trinh_do_id) if trinh_do_id else None

            hoso, created = HoSoHocTap.objects.get_or_create(
                khach_hang=khach_hang,
                defaults={
                    'ho_ten': ho_ten,
                    'ngay_sinh': ngay_sinh,
                    'gioi_tinh': gioi_tinh,
                    'ngon_ngu_hoc': ngon_ngu,
                    'trinh_do': trinh_do,
                }
            )
            if not created:
                return JsonResponse({'success': False, 'message': 'Hồ sơ đã tồn tại cho khách hàng này.'}, status=400)
            return JsonResponse({'success': True, 'id': hoso.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_GET
@api_view(['GET'])
@login_required
def data_HoSo(request):
    khach_hang = request.user
    data = HoSoHocTap.objects.filter(khach_hang_id=khach_hang.id).values(
        'id', 'ho_ten', 'ngay_sinh', 'gioi_tinh', 'khach_hang_id', 'trinh_do_id', 'ngon_ngu_hoc_id'
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
