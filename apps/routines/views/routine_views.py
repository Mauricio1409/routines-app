# APIView - Permite tener 4 funciones HTTP (GET, POST, PUT, DELETE) (Todo manual)
# ViewSet - Permite tener 5 funciones HTTP (list, create, retrieve, update, destroy) (Mannual) y agregar mas con @Action
# ModelViewSet - Igual que ViewSet pero con funcionalidades CRUD automáticas (No manual) y con funcionalidades extra
# por serializers (Validaciones automáticas)
from rest_framework.permissions import  IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from apps.routines.models import Routine
from apps.routines.serializers.routine_serializers import RoutineSerializer, RoutineDetailSerializer

# /routines/
class RoutineViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Evita error en drf-yasg (Swagger) cuando user = AnonymousUser
        if getattr(self, 'swagger_fake_view', False):
            return Routine.objects.none()

        return Routine.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RoutineDetailSerializer
        return RoutineSerializer





