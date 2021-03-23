from django.db import models

class UniqueID(models.Model):
    unique_code = models.CharField(max_length=6, unique=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.unique_code

class QRCode(models.Model):
    qr_id = models.OneToOneField(UniqueID, on_delete=models.CASCADE, primary_key=True, related_name="qrcode")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=80, null=True, blank=True)
    contact = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return self.name