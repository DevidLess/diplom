from django.urls import path
from .views import AgenciesListView, AboutView, PrivacyView

app_name = "pages"

urlpatterns = [
    path("agencies/", AgenciesListView.as_view(), name="agencies_list"),
    path("about/", AboutView.as_view(), name="about"),
    path("privacy/", PrivacyView.as_view(), name="privacy"),
]
