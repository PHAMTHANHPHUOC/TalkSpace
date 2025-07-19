from django.db import models
from .LichSuHoiThoai import LichSuHoiThoai

class TinNhanHoiThoai(models.Model):
    LOAI_NGUOI_GUI_CHOICES = [
        ('user', 'Người dùng'),
        ('ai', 'AI'),
    ]
    
    LOAI_TIN_NHAN_CHOICES = [
        ('text', 'Văn bản'),
        ('audio', 'Âm thanh'),
    ]
    
    hoi_thoai = models.ForeignKey(LichSuHoiThoai, on_delete=models.CASCADE, related_name='tin_nhan')
    nguoi_gui = models.CharField(max_length=10, choices=LOAI_NGUOI_GUI_CHOICES)
    noi_dung = models.TextField()
    thoi_gian_gui = models.DateTimeField(auto_now_add=True)
    loai_tin_nhan = models.CharField(max_length=10, choices=LOAI_TIN_NHAN_CHOICES, default='text')
    duong_dan_audio = models.CharField(max_length=500, null=True, blank=True)
    
    class Meta:
        db_table = 'tin_nhan_hoi_thoai'
        verbose_name = 'Tin nhắn hội thoại'
        verbose_name_plural = 'Tin nhắn hội thoại'
        ordering = ['thoi_gian_gui']
    
    def __str__(self):
        return f"Tin nhắn từ {self.nguoi_gui} - {self.thoi_gian_gui.strftime('%H:%M:%S')}"
    
    def la_tin_nhan_ai(self):
        """Kiểm tra có phải tin nhắn từ AI không"""
        return self.nguoi_gui == 'ai'
    
    def la_tin_nhan_nguoi_dung(self):
        """Kiểm tra có phải tin nhắn từ người dùng không"""
        return self.nguoi_gui == 'user'
    
    def la_tin_nhan_audio(self):
        """Kiểm tra có phải tin nhắn audio không"""
        return self.loai_tin_nhan == 'audio'
    
    def co_audio(self):
        """Kiểm tra có file audio không"""
        return bool(self.duong_dan_audio)
