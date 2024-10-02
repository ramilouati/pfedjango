from django.db import models





class Assure(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    tel = models.CharField(max_length=20)
    nom_assurance = models.CharField(max_length=255,default="")
    police = models.CharField(max_length=255,default="")
    agence = models.CharField(max_length=255,default="")
    date_debut_attestation = models.DateField(default="01-01-2001")
    date_fin_attestation = models.DateField(default="01-01-2001")

    def __str__(self):
        return f"{self.nom} {self.prenom}"
 


# class User(models.Model):
#     nom = models.CharField(max_length=255)
#     prenom = models.CharField(max_length=255)
#     date_naissance = models.DateField()
#     cin = models.CharField(max_length=20)
#     tel = models.CharField(max_length=20)
#     address = models.CharField(max_length=255)
#     date_permis = models.DateField()

#     def __str__(self):
#         return f"{self.nom} {self.prenom}"

# class Constat(models.Model):
#     id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
#     date = models.DateField()
#     lieu = models.CharField(max_length=255)
#     temoin = models.TextField(null=True, blank=True)
#     croquis = models.FileField(upload_to='constat_croquis/', null=True, blank=True)

#     vehicleA = models.FileField(upload_to='constat_vehicleA/', null=True, blank=True)
#     vehicleB = models.FileField(upload_to='constat_vehicleB/', null=True, blank=True)

#     def __str__(self):
#         return f"Constat - {self.date} - {self.lieu}"




# class DegatApparent(models.Model):
#     constat = models.ForeignKey(Constat, related_name='degats', on_delete=models.CASCADE)
#     degat = models.TextField()
#     images_accident = models.ImageField(upload_to='accident_images/')
#     videos_accident = models.FileField(upload_to='accident_videos/', null=True, blank=True)

#     def __str__(self):
#         return self.degat

# class Conversation(models.Model):
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(User, related_name='conversations', on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Conversation at {self.timestamp}"
