from rest_framework.exceptions import APIException


class RoutineNotFoundException(APIException):
    status_code = 404
    default_detail = "La rutina solicitada no fue encontrada."
    default_code = "routine_not_found"

class RoutinePermissionDeniedException(APIException):
    status_code = 403
    default_detail = "No tienes permiso para acceder a esta rutina."
    default_code = "routine_permission_denied"

class WorkoutNotFoundException(APIException):
    status_code = 404
    default_detail = "El entrenamiento solicitado no fue encontrado."
    default_code = "workout_not_found"