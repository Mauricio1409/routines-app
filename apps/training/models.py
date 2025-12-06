from django.db import models
from django.conf import settings
from apps.exercises.models import Exercise
from apps.routines.models import Workout


class WorkoutSession(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sessions'
    )

    workout = models.ForeignKey(
        Workout,
        on_delete=models.SET_NULL,  # AHORA sí cascada
        related_name='sessions',
        null = True,
        blank = True,
    )

    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha y Hora"
    )

    duration = models.DurationField(
        null=False,
        blank=False,
        verbose_name="Duración"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Notas de la sesión",
        help_text="Ej: Me sentí cansado, dormí mal anoche."
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        fecha = self.date.strftime("%d/%m/%Y")
        return f"{fecha} - {self.workout.name if self.workout else 'Entrenamiento Libre'}"


class ExerciseLog(models.Model):

    session = models.ForeignKey(
        WorkoutSession,
        on_delete=models.CASCADE,
        related_name='logs'
    )

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.PROTECT
    )

    set_number = models.PositiveIntegerField(verbose_name="# Serie")
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Peso (kg)")
    reps = models.PositiveIntegerField(verbose_name="Repeticiones")

    rpe = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="RPE (1-10)"
    )

    class Meta:
        ordering = ['set_number']
        verbose_name = "Registro de Serie"
        verbose_name_plural = "Registros de Series"

    def __str__(self):
        return f"{self.exercise.name}: {self.weight_kg}kg x {self.reps}"
