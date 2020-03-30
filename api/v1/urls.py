from django.urls import re_path

from api.v1 import views

app_name = "v1"
urlpatterns = [
    re_path(r"^attack/?$", views.AttackView.as_view(), name="attack"),
    re_path(r"^stats/?$", views.StatsView.as_view(), name="stats"),
]
