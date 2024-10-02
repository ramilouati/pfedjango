from django.contrib import admin

from Etretien.models import Entretien
from Vehicles.models import Vehicle, VehicleImage



admin.site.register(Vehicle)
admin.site.register(VehicleImage)

# Register your models here.
