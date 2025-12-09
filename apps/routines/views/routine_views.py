# APIView - Permite tener 4 funciones HTTP (GET, POST, PUT, DELETE) (Todo manual)
# ViewSet - Permite tener 5 funciones HTTP (list, create, retrieve, update, destroy) (Mannual) y agregar mas con @Action
# ModelViewSet - Igual que ViewSet pero con funcionalidades CRUD automáticas (No manual) y con funcionalidades extra
# por serializers (Validaciones automáticas)
from rest_framework.decorators import action
from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from apps.routines.services.routine_service import RoutineService


# /routines/
class RoutineViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    service = RoutineService()

    def list(self, request):
        routines = self.service.get_all(user=request.user, query_params=request.query_params)
        return Response(routines, status=status.HTTP_200_OK)

    def create(self, request):
        routine = self.service.create(request.data, user=request.user)
        return Response(routine, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        routine = self.service.get_by_id(pk=pk, user=request.user)
        return Response(routine, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        routine = self.service.update(pk=pk, data=request.data, user=request.user)
        return Response(routine, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        self.service.delete(pk=pk, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"], url_path="workouts")
    def workouts(self, request, pk=None):
        workouts = self.service.get_workout_by_routine(pk=pk, user=request.user,query_params=request.query_params)
        return Response(workouts, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="sessions")
    def sessions(self, request, pk=None):
        sessions = self.service.get_sessions_by_routine(pk=pk, user=request.user)
        return Response(sessions, status=status.HTTP_200_OK)








