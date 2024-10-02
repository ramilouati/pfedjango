from django.urls import path
from django.conf.urls.static import static

from Vehicles.views import VehicleListView
from insurance_app import settings

urlpatterns = [
    path('vehicles/', VehicleListView.as_view(), name='vehicle_list'),
    path('vehicles/<int:vehicle_id>/', VehicleListView.as_view(), name='vehicle_detail'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)