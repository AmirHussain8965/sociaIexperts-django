from django.db import models
from django.contrib.auth.models import User

class MasterSignupCode(models.Model):
    code = models.CharField(max_length=100, help_text="Global registration code required for new users.")

    def save(self, *args, **kwargs):
        self.pk = 1
        super(MasterSignupCode, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass # Prevent deletion of the master code

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1, defaults={'code': 'MASTERCODE2026'})
        return obj

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Master Registration Code"
        verbose_name_plural = "Master Registration Code"


class OTPRecord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.user.username}"
