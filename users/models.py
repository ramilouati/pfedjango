from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, cin, password=None, **extra_fields):
        if not cin:
            raise ValueError('The CIN must be set')
        user = self.model(cin=cin, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cin, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(cin, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # Remove the default username field
    cin = models.CharField(max_length=20, unique=True)
    tel = models.CharField(max_length=20)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    date_naissance = models.DateField()
    address = models.CharField(max_length=255)
    npermis = models.CharField(max_length=255)
    date_permis = models.DateField(default="2001-01-10")
    role = models.CharField(max_length=255, default="Conducteur")
    USERNAME_FIELD = 'cin'  # Use 'cin' as the unique identifier
    REQUIRED_FIELDS = ['tel', 'date_naissance', 'nom', 'prenom']

    objects = CustomUserManager()  # Add the custom user manager

    def __str__(self):
        return f"{self.nom} {self.prenom}"
