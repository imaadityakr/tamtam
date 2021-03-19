from django.db import models

class QRCodes(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=80, null=True, blank=True)
    contact = models.CharField(max_length=80, null=True, blank=True)
    qrcode = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return self.name