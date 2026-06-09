from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path("tos/", RedirectView.as_view(url="/terms/", permanent=True)),
]
