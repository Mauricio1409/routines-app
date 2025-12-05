from django.db import models
import uuid

# Create your models here.

class Exercises(models.Model):
    class MuscleGroups(models.TextChoices):
        CHEST = 'CHEST', 'Pecho'
        BACK = 'BACK', 'Espalda'
        LEGS = 'LEGS', 'Piernas'
        SHOULDERS = 'SHOULDERS', 'Hombros'
        ARMS = 'ARMS', 'Brazos'
        ABS = 'ABS', 'Abdominales'
        FULL_BODY = 'FULL_BODY', 'Cuerpo Completo'
        OTHER = 'OTHER', 'Otro'

    class EquipmentType(models.TextChoices):
        DUMBBELL = 'DUMBBELL', 'Mancuernas'
        BARBELL = 'BARBELL', 'Barra'
        MACHINE = 'MACHINE', 'Máquina'
        BODYWEIGHT = 'BODYWEIGHT', 'Peso Corporal'
        OTHER = 'OTHER', 'Otro'

    class ExerciseType(models.TextChoices):
        STRENGTH = 'STRENGTH', 'Fuerza'
        CARDIO = 'CARDIO', 'Cardio'
        FLEXIBILITY = 'FLEXIBILITY', 'Flexibilidad'
        BALANCE = 'BALANCE', 'Equilibrio'
        OTHER = 'OTHER', 'Otro'


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    video_url = models.URLField(max_length=1000, null=True, blank=True)

    muscle_group = models.CharField(
        max_length=20,
        choices=MuscleGroups.choices,
        default=MuscleGroups.OTHER
    )

    equipment_type = models.CharField(
        max_length=20,
        choices=EquipmentType.choices,
        default=EquipmentType.OTHER
    )

    exercise_type = models.CharField(
        max_length=20,
        choices=ExerciseType.choices,
        default=ExerciseType.OTHER
    )

    def __str__(self):
        return self.name