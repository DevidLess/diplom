from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from project import settings
from accounts import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("website.urls")),
    path("pages/", include("pages.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),
    path("lawyers/", include("lawyer.urls")),

    path("login/", views.SiteLoginView.as_view(), name="login"),
    path("logout/", views.SiteLogoutView.as_view(), name="logout"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
