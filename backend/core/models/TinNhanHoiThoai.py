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
    cam_xuc_ai = models.CharField(max_length=50, null=True, blank=True, help_text='Cảm xúc AI thể hiện (vui, buồn, ngạc nhiên...)')
    avatar_ai = models.CharField(max_length=500, null=True, blank=True, help_text='Đường dẫn avatar AI (nếu có)')
    
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
    
    def co_cam_xuc_ai(self):
        """Kiểm tra có thông tin cảm xúc AI không"""
        return bool(self.cam_xuc_ai)
    
    def co_avatar_ai(self):
        """Kiểm tra có avatar AI không"""
        return bool(self.avatar_ai)
    
    def lay_cam_xuc_ai(self):
        """Lấy cảm xúc AI, trả về 'neutral' nếu không có"""
        return self.cam_xuc_ai or 'neutral'
    
    def lay_avatar_ai(self):
        """Lấy đường dẫn avatar AI, trả về avatar mặc định nếu không có"""
        return self.avatar_ai or '/static/images/AI.jpg'
