from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from apps.training.models import WorkoutSession
from apps.training.serializers.training_serializers import WorkOutSessionSerializer, WorkOutSessionDetailSerializer



class WorkOutSessionView(ViewSet):
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None):
        try:

            workout = (
                WorkoutSession.objects
                .prefetch_related("logs__exercise")
                .get(id=pk)
            )

            if workout.user != request.user:
                return Response(
                    {"detail": "No tienes permiso para ver esta sesión de entrenamiento."},
                    status=403
                )

            serializer = WorkOutSessionDetailSerializer(workout)
            return Response(serializer.data, status=200)

        except WorkoutSession.DoesNotExist:
            return Response({"detail": "Sesión no encontrada."}, status=404)

        except Exception:
            return Response({"detail": "Error interno."}, status=500)


    def create(self, request):
        try:
            serializer = WorkOutSessionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            data = serializer.validated_data

            session = WorkoutSession.objects.create(
                **data,
                user=request.user
            )

            output = WorkOutSessionSerializer(session)

            return Response(output.data, status=201)

        except Exception as e:
            return Response({"detail": "Error al crear la sesión."}, status=500)


    def update(self, request, pk=None):
        try:
            session = WorkoutSession.objects.get(id=pk)

            if session.user != request.user:
                return Response(
                    {"detail": "No tienes permiso para modificar esta sesión de entrenamiento."},
                    status=403
                )

            serializer = WorkOutSessionSerializer(session, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            session.save(
                **serializer.validated_data
            )

            return Response(serializer.data, status=200)

        except WorkoutSession.DoesNotExist:
            return Response({"detail": "Sesión no encontrada."}, status=404)

        except Exception:
            return Response({"detail": "Error al actualizar la sesión."}, status=500)

