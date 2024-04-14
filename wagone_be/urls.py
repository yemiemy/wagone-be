from django.urls import path, include, reverse_lazy
from django.views.generic.base import RedirectView
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("admin:index"))),
    path("admin/", admin.site.urls),
    path("api/v1/account/", include("accounts.urls")),
    path("api/v1/chat/", include("chat.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

admin.site.site_header = "WagOne administration"
admin.site.site_title = "WagOne site admin"
admin.site.index_title = "Site administration"
