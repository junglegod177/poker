from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url="login")),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path('register/', views.register, name='register'),
    path("tables/", views.tables, name="tables"),
    path("table/", views.table, name="table"),
    path("error/", views.error, name="error")
]
