from django.contrib import admin

# Register your models here.
from accounts.models import User, UserContact


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_email_verified",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )

    class Meta:
        model = User


admin.site.register(User, UserAdmin)
admin.site.register(UserContact)
