from ..repositories.workout_session_repository import WorkOutSessionRepository
from ..serializers.training_serializers import (WorkOutSessionSerializer, WorkOutSessionDetailSerializer, 
                                                WorkOutSessionUpdateSerializer, ExerciseLogDetailSerializer)

class WorkOutSessionService:
    def __init__(self):
        self.repository = WorkOutSessionRepository()
        
    def create_session(self, data, user):
        serializer = WorkOutSessionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        workout = serializer.validated_data['workout']
        if workout.routine.user != user:
            raise Exception("You do not have permission to create a session for this workout.")
        
        new_session = {
            "user": user,
            **serializer.validated_data
        }
        
        created_session = self.repository.create(new_session)
        return WorkOutSessionSerializer(created_session).data
    
    def get_sessions_by_user(self, user):
        sessions = self.repository.get_sessions_by_user(user)
        return WorkOutSessionSerializer(sessions, many=True).data
    
    def get_session_detail(self, pk, user):
        session = self.repository.get_detail_by_id(pk)
        if not session:
            raise Exception("Session not found.")
        
        if session is None or session.user != user:
            raise Exception("Session not found or you do not have permission to access it.")
        
        return WorkOutSessionDetailSerializer(session).data
    
    def update_session(self, pk, data, user):
        serilizer = WorkOutSessionUpdateSerializer(data=data, partial=True)
        serilizer.is_valid(raise_exception=True)
        
        session = self.repository.get_detail_by_id(pk)
        if not session:
            raise Exception("Session not found.")
        if session.user != user:
            raise Exception("You do not have permission to update this session.")
        
        updated_session = self.repository.update(session, serilizer.validated_data)
        return WorkOutSessionSerializer(updated_session).data
    
    def delete_session(self, pk, user):
        session = self.repository.get_detail_by_id(pk)
        if not session:
            raise Exception("Session not found.")
        if session.user != user:
            raise Exception("You do not have permission to delete this session.")
        
        self.repository.delete(session)
        return
    
    def get_exercises_logs_by_session(self, pk, user):
        session = self.repository.get_detail_by_id(pk)
        if not session:
            raise Exception("Session not found.")
        
        if session.user != user:
            raise Exception("You do not have permission to access this session's exercises.")
        
        exercises = self.repository.get_exercises_logs_by_session(session)
        
        return WorkOutSessionDetailSerializer(session).data
    
    
        