from django.urls import path
from api.views import verify_title_view

urlpatterns = [
    path('verify-title/', verify_title_view, name='verify-title'),
]
