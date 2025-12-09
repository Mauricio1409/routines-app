from core.repositories.base_repository import BaseRepository
from apps.training.models import WorkoutSession

class WorkOutSessionRepository(BaseRepository):
    def __init__(self):
        super().__init__(WorkoutSession)
        
    def get_sessions_by_user(self, user):
        return self.model.objects.filter(user=user).order_by('-date')
    
    def get_detail_by_id(self, pk):
        return self.model.objects.select_related('user').prefetch_related('logs__exercise').filter(id=pk).first()
    
    def get_exercises_logs_by_session(self, session):
        return session.logs.all().order_by('session__workout__exercises__order', 'set_number')
        