from django.urls import path
# from .views.dashboard import DashboardView
from . import views
from dictionary.views import articles, user_plants


app_name = "encyklopedia"

urlpatterns = [
    # path("", articles.homepage, name="homepage"),
    path('', articles.PostList.as_view(), name='home'),
    path('<slug:slug>/', articles.post_detail, name='post_detail'),

    path('add-plant/<slug:slug>/', user_plants.add_to_plantList, name='add_to_plant_list'),
    path('remove-plant/<slug:slug>/', user_plants.remove_from_plantList, name='remove_from_plant_list'),
]