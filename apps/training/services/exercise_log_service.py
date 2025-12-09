from ..repositories.exercise_log_repository import ExerciseLogRepository
from ..serializers.training_serializers import ExerciseLogSerializer, ExerciseLogUpdateSerializer
from apps.routines.services.workout_exercises_service import WorkOutExercisesService
from .workout_session import WorkOutSessionService

class ExerciseLogService:
    def __init__(self):
        self.repository = ExerciseLogRepository()
        self.workout_exercises_service = WorkOutExercisesService()
        self.session_service = WorkOutSessionService()
        
    def create_log(self,pk, data, user):
        serializer = ExerciseLogSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        session = self.session_service.repository.get_detail_by_id(pk)
        if not session:
            raise Exception("Session not found.")
        
        if session.user != user:
            raise Exception("You do not have permission to create a log for this session.")
        
        exercise = serializer.validated_data['exercise']
        
        exists = self.workout_exercises_service.exists_exercise_in_workout(session.workout, exercise)
        if not exists:
            raise Exception("The exercise is not part of the workout associated with this session.")
        
        new_log = {
            **serializer.validated_data,
            "session": session
        }
        
        created_log = self.repository.create(new_log)
        return ExerciseLogSerializer(created_log).data
    
    def update_log(self, pk, data, user, session_pk):
        serializer = ExerciseLogUpdateSerializer(data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        session = self.session_service.repository.get_detail_by_id(session_pk)
        if not session:
            raise Exception("Session not found.")
        
        if session.user != user:
            raise Exception("You do not have permission to update this exercise log.")
        
        log = self.repository.get_by_id(pk)
        if not log:
            raise Exception("Exercise log not found.")
        
        if log.session != session:
            raise Exception("This log does not belong to the specified session.")
        
        
        updated_log = self.repository.update(log, serializer.validated_data)
        return ExerciseLogSerializer(updated_log).data
    
    def delete_log(self, pk, user, session_pk):
        session = self.session_service.repository.get_detail_by_id(session_pk)
        if not session:
            raise Exception("Session not found.")
        
        if session.user != user:
            raise Exception("You do not have permission to delete this exercise log.")
        
        log = self.repository.get_by_id(pk)
        if not log:
            raise Exception("Exercise log not found.")
        
        if log.session != session:
            raise Exception("This log does not belong to the specified session.")
        
        self.repository.delete(log)
        return
        
        
        
        
        
