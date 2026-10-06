from django.contrib import admin
from .models import EmailVerificationToken, PasswordResetToken, SessionToken

admin.site.register(EmailVerificationToken)
admin.site.register(PasswordResetToken)
admin.site.register(SessionToken)
