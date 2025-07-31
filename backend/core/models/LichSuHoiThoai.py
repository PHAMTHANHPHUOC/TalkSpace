from django.db import models
from .KhachHang import KhachHang
from .BaiHoc import BaiHoc

class LichSuHoiThoai(models.Model):
    nguoi_dung = models.ForeignKey(KhachHang, on_delete=models.CASCADE, related_name='lich_su_hoi_thoai')
    bai_hoc = models.ForeignKey(BaiHoc, on_delete=models.CASCADE, related_name='lich_su_hoi_thoai')
    thoi_gian_bat_dau = models.DateTimeField(auto_now_add=True)
    thoi_gian_ket_thuc = models.DateTimeField(null=True, blank=True)
    diem_phan_xa = models.FloatField(default=0.0)
    hoan_thanh = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'lich_su_hoi_thoai'
        verbose_name = 'Lịch sử hội thoại'
        verbose_name_plural = 'Lịch sử hội thoại'
        ordering = ['-thoi_gian_bat_dau']
    
    def __str__(self):
        return f"Hội thoại của {self.nguoi_dung.email} - Bài học: {self.bai_hoc.ten_bai_hoc}"
    
    def tinh_thoi_luong(self):
        """Tính thời lượng buổi học"""
        if self.thoi_gian_ket_thuc:
            return self.thoi_gian_ket_thuc - self.thoi_gian_bat_dau
        return None
    
    def ket_thuc_buoi_hoc(self):
        """Kết thúc buổi học"""
        from django.utils import timezone
        self.thoi_gian_ket_thuc = timezone.now()
        self.hoan_thanh = True
        self.save()
    
    def cap_nhat_diem_phan_xa(self, diem):
        """Cập nhật điểm phản xạ"""
        self.diem_phan_xa = diem
        self.save()
