from django.db import models
from .ChuDe import ChuDe
from .CapDo import CapDo
from .NgonNgu import NgonNgu
from .KhachHang import KhachHang

class BaiHoc(models.Model):
    ten_bai_hoc = models.CharField(max_length=255)
    chu_de = models.ForeignKey(ChuDe, on_delete=models.CASCADE, related_name='bai_hoc')
    cap_do = models.ForeignKey(CapDo, on_delete=models.SET_NULL, null=True, related_name='bai_hoc')
    noi_dung = models.TextField()
    ngon_ngu = models.ForeignKey(NgonNgu, on_delete=models.CASCADE, related_name='bai_hoc')
    ngay_tao = models.DateTimeField(auto_now_add=True)
    nguoi_tao = models.ForeignKey(KhachHang, on_delete=models.SET_NULL, null=True, related_name='bai_hoc_tao')

    def __str__(self):
        return self.ten_bai_hoc
