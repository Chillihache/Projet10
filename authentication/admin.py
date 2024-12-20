from django.contrib import admin
from authentication.models import User


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ("created_time",)


admin.site.register(User, UserAdmin)
