from django.db import models

class Vehicle(models.Model):
    assure = models.ForeignKey('insurance.Assure', on_delete=models.CASCADE, null=True)
    marque = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    date_fabrication = models.DateField()
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='vehicle_images/', null=True, blank=True)
    


    def __str__(self):
        return self.marque

class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='vehicle_images/')  # Specify the directory where images will be stored

    def __str__(self):
        return f"Image for {self.vehicle.marque}"
