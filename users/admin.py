from django.contrib import admin
from .models import User, Payment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_staff']
    fields = ['email', 'password', 'is_staff', 'groups']

admin.site.register(Payment)