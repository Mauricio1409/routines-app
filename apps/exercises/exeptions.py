from rest_framework.exceptions import APIException


class ExerciseNotFoundError(APIException):
    status_code = 404
    default_detail = "El ejercicio solicitado no fue encontrado."
    default_code = "exercise_not_found"