from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from apps.exercises.models import Exercise


User = get_user_model()

# Create your models here.
class Routine(models.Model):
    class Goal(models.TextChoices):
        HYPERTROPHY = 'HYPERTROPHY', 'Hipertrofia'
        STRENGTH = 'STRENGTH', 'Fuerza'
        WEIGHT_LOSS = 'WEIGHT_LOSS', 'Pérdida de Peso'
        ENDURANCE = 'ENDURANCE', 'Resistencia'
        MAINTENANCE = 'MAINTENANCE', 'Mantenimiento'

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='routines'
    )

    name = models.CharField(max_length=100, verbose_name="Nombre de la Rutina")
    description = models.TextField(blank=True, null=True)
    goal = models.CharField(
        max_length=20,
        choices=Goal.choices,
        default=Goal.HYPERTROPHY,
        verbose_name="Objetivo de la Rutina"
    )

    start_date = models.DateField(verbose_name="Fecha de inicio")
    end_date = models.DateField(blank=True, null=True, verbose_name="Fecha de fin")

    def __str__(self):
        return f"{self.name} ({self.get_goal_display()})"


class Workout(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='workouts')
    name = models.CharField(max_length=100, verbose_name="Nombre del Entrenamiento")
    day_order = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(7)],
    )

    class Meta:
        unique_together = ('routines', 'day_order')
        # Agrega un constraint que no me permite que se registre dos días con el mismo número en la misma rutina
        ordering = ['day_order']

    def __str__(self):
        return f"{self.name} - Día {self.day_order} de {self.routines.name}"


class WorkoutExercise(models.Model):

    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name='exercises'
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField(default=1, verbose_name="Orden en la sesión")

    sets = models.PositiveIntegerField(default=4, verbose_name="Series")
    reps_min = models.PositiveIntegerField(default=8, verbose_name="Reps Mínimas")
    reps_max = models.PositiveIntegerField(default=12, verbose_name="Reps Máximas")
    rest_time = models.PositiveIntegerField(default=60, verbose_name="Descanso (segundos)")

    notes = models.CharField(
        max_length=255,
        blank=True,
        help_text="Ej: 'Bajar lento', 'Aguantar 1 seg arriba'"
    )

    class Meta:
        ordering = ['order']
        unique_together = ['workout', 'order']

    def __str__(self):
        return f"{self.order}. {self.exercise.name} ({self.sets}x{self.reps_min}-{self.reps_max})"

