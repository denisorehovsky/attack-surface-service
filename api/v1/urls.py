from django.urls import path

from api.v1 import views

app_name = "v1"
urlpatterns = [
    path("attack/", views.AttackView.as_view(), name="attack"),
    path("stats/", views.StatsView.as_view(), name="stats"),
]
