from django.contrib import admin

from .models import UserDetails

# Register your models here.


class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ['user', 'address']


admin.site.register(UserDetails, UserDetailsAdmin)
