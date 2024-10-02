from django.db import models

# Create your models here.

class Constat(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    date = models.DateField( null=True)
    lieu = models.CharField(max_length=255 ,null=True)
    codeA = models.CharField(max_length=255 ,null=True)
    codeB = models.CharField(max_length=255 ,null=True)
    codeB = models.CharField(max_length=255 ,null=True)
    vehicleA = models.FileField(upload_to='constat_vehicleA/', null=True, blank=True)
    vehicleB = models.FileField(upload_to='constat_vehicleB/', null=True, blank=True)
    cinA = models.CharField(max_length=255 ,null=True)
    cinB = models.CharField(max_length=255 ,null=True)
    def __str__(self):
        return f"Constat - {self.date} - {self.lieu}"

