from django.db import models
from .NgonNgu import NgonNgu

class ChuDe(models.Model):
    ten_chu_de = models.CharField(max_length=255)
    ngon_ngu = models.ForeignKey(NgonNgu, on_delete=models.CASCADE, related_name='chu_de')

    def __str__(self):
        return self.ten_chu_de
