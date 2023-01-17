from django.urls import path
# from .views.dashboard import DashboardView
from . import views
from dictionary.views import articles

app_name = "encyklopedia"

urlpatterns = [
    path("", articles.homepage, name="homepage"),
]