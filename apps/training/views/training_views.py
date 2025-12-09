from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from ..services.workout_session import WorkOutSessionService
from rest_framework.decorators import action
from ..services.exercise_log_service import ExerciseLogService



class WorkOutSessionView(ViewSet):
    permission_classes = (IsAuthenticated,)
    service = WorkOutSessionService()
    exercise_log_service = ExerciseLogService()
    
    def list(self, request):
        sessions = self.service.get_sessions_by_user(request.user)
        return Response(sessions, status=200)

    def retrieve(self, request, pk=None):
        session = self.service.get_session_detail(pk, request.user)
        return Response(session, status=200)


    def create(self, request):
        session = self.service.create_session(request.data, request.user)
        return Response(session, status=201)
    
    def update(self, request, pk=None):
        session = self.service.update_session(pk, request.data, request.user)
        return Response(session, status=200)
    
    def destroy(self, request, pk=None):
        self.service.delete_session(pk, request.user)
        return Response(status=204)
    
    @action(detail=True, methods=['get', 'post'], url_path='exercises')
    def get_exercises(self, request, pk=None):
        if request.method == 'GET':
            session = self.service.get_exercises_logs_by_session(pk, request.user)
            return Response(session, status=200)
        
        if request.method == 'POST':
            session = self.exercise_log_service.create_log(pk, request.data, request.user)
            return Response(session, status=201)
        
    @action(detail=True, methods=['put', 'delete'], url_path='exercises/(?P<log_pk>[^/.]+)')
    def modify_exercise_log(self, request, pk=None, log_pk=None):
        if request.method == 'PUT':
            log = self.exercise_log_service.update_log(log_pk, request.data, request.user, pk)
            return Response(log, status=200)
        
        if request.method == 'DELETE':
            self.exercise_log_service.delete_log(log_pk, request.user, pk)
            return Response(status=204)
    
    