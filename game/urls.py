from django.urls import path

from . import views

urlpatterns = [
    path("table", views.table, name="table"),
    path("error", views.error, name="error")
]
