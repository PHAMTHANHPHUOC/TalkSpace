from django.db import models

class NgonNgu(models.Model):
    ten_ngon_ngu = models.CharField(max_length=100, unique=True)
    ma_ngon_ngu = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.ten_ngon_ngu
