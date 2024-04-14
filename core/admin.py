from django.contrib import admin
from django.utils.translation import gettext_lazy

# Register your models here.


class WagOneAdminSite(admin.AdminSite):
    site_title = gettext_lazy("WagOne site admin")
    site_header = gettext_lazy("WagOne administration")
    index_title = gettext_lazy("Site administration")
    site_url = None


admin_site = WagOneAdminSite(name="wagone_admin")
