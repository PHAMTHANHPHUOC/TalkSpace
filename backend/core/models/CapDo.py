from django.db import models

class CapDo(models.Model):
    ten_cap_do = models.CharField(max_length=100)
    mo_ta = models.TextField(blank=True)

    def __str__(self):
        return self.ten_cap_do
