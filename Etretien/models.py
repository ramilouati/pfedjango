from django.db import models

from Vehicles.models import Vehicle

class Entretien(models.Model):
    nom_entretien = models.CharField(max_length=255)
    kilometrage = models.IntegerField()
    date = models.DateField()
    vehicle = models.ForeignKey(Vehicle, related_name='entretiens', on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_entretien
