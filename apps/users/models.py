from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')

        email = self.normalize_email(email)
        # Aquí está el truco: creamos el modelo SIN pasar username explícitamente
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


# 2. Tu modelo de Usuario
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Hacemos que el username ya no sea obligatorio en la base de datos
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name='Correo Electrónico')

    # Conectamos el nuevo Manager
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Ya no pedimos username aquí

    def __str__(self):
        return self.email

class BodyMetric(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='metrics'
    )
    date = models.DateField(auto_now_add=True, verbose_name="Fecha de medición")

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Peso (kg)",
        null=False,
        blank=False
    )

    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Altura (cm)",
        null=False,
        blank=False
    )

    body_fat_percentage = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name="% Grasa Corporal"
    )

    class Meta:
        # Opciones del modelo:
        # - ordering: orden por defecto en las consultas (ej. ['-date'])
        # - verbose_name / verbose_name_plural: nombres legibles en el admin
        # - db_table: nombre explícito de la tabla en la base de datos
        # - unique_together / constraints: restricciones de unicidad a nivel de tabla
        # - indexes: índices para optimizar consultas
        # - permissions: permisos personalizados asociados al modelo
        # - get_latest_by: campo usado por Model.objects.latest()
        ordering = ['-date']
        verbose_name = "Medida Corporal"
        verbose_name_plural = "Medidas Corporales"

    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.weight}kg"
