from django.contrib import admin
from django_google_plus.models import UserGoogleID

class AdminUserGoogleID(admin.ModelAdmin):
    model = UserGoogleID

admin.site.register(UserGoogleID, AdminUserGoogleID)
