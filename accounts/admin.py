from django.contrib import admin
from .models import OTPRecord, MasterSignupCode

@admin.register(MasterSignupCode)
class MasterSignupCodeAdmin(admin.ModelAdmin):
    list_display = ('code',)

admin.site.register(OTPRecord)
