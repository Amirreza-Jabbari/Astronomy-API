from django.urls import path
from .views import AstronomyDataView

urlpatterns = [
    path('astronomy/', AstronomyDataView.as_view(), name='astronomy-data'),
]