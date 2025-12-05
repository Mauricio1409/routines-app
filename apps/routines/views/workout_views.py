from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from apps.routines.models import Workout, WorkoutExercise
from apps.routines.serializers.workout_serializer import WorkoutSerialzier, WorkoutExerciseSerializer

class WorkOutViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkoutSerialzier

    def get_queryset(self):
        user = self.request.user
        # OPTIMIZACIÓN 1: 'routine__user' (singular) porque Workout tiene una FK a Routine
        # OPTIMIZACIÓN 2: prefetch_related para traer los ejercicios hijos y evitar problema N+1
        # OPTIMIZACIÓN 3: select_related para traer los datos de la rutina padre en la misma query
        return ((Workout.objects.filter(routines__user=user)
                .select_related('routines'))
                .prefetch_related('exercises__exercise')) # Asumiendo que 'exercises' es el related_name en WorkoutExercise


    def get_serializer_class(self):
        if self.action == 'retrieve':
            from apps.routines.serializers.workout_serializer import WorkOutDetailSerializer
            return WorkOutDetailSerializer
        return WorkoutSerialzier


    def perform_create(self, serializer):
        user = self.request.user
        routine = serializer.validated_data.get('routines')
        if routine.user != user:
            raise PermissionDenied("No tienes permiso para agregar un workout a esta rutina.")
        serializer.save()

class WorkoutExerciseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class =  WorkoutExerciseSerializer

    def get_queryset(self):
        user = self.request.user
        # OPTIMIZACIÓN 4: select_related para traer el workout y el ejercicio base (catalogo)
        return WorkoutExercise.objects.filter(workout__routines__user=user)\
            .select_related('workout', 'exercise')

    def perform_create(self, serializer):
        user = self.request.user
        workout = serializer.validated_data.get('workout')
        if workout.routines.user != user:
            raise PermissionDenied("No tienes permiso para agregar un ejercicio a este workout.")
        serializer.save()