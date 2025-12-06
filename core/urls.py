
from django.contrib import admin
from django.urls import path, include

from apps.users.urls import metrics_router
from apps.routines.urls import routine_router
from apps.training.urls import session_router
from apps.exercises.urls import exercises_router


urlpatterns = [
    path('admin/', admin.site.urls),

    # Autenticación con Djoser
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),

    # APIs de las apps
    path('api/', include(exercises_router.urls)),
    path('api/', include(metrics_router.urls)),
    path('api/', include(routine_router.urls)),
    path('api/', include(session_router.urls)),
]
