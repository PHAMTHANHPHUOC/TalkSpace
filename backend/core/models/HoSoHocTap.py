from django.db import models
from .KhachHang import KhachHang
from .NgonNgu import NgonNgu
from .CapDo import CapDo

class HoSoHocTap(models.Model):
    khach_hang = models.ForeignKey(KhachHang, on_delete=models.CASCADE, related_name='ho_so_hoc_tap')
    ho_ten = models.CharField(max_length=255)
    ngay_sinh = models.DateField(null=True, blank=True)
    gioi_tinh = models.CharField(max_length=10, choices=[('Nam', 'Nam'), ('Nu', 'Nữ'), ('Khac', 'Khác')], default='Khac')
    ngon_ngu_hoc = models.ForeignKey(NgonNgu, on_delete=models.SET_NULL, null=True, related_name='ho_so_hoc_tap')
    # trinh_do = models.ForeignKey(CapDo, on_delete=models.SET_NULL, null=True, related_name='ho_so_hoc_tap')

    def __str__(self):
        return self.ho_ten
