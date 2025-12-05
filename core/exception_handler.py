from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        detail = response.data

        if isinstance(detail, dict) and "detail" not in detail:
            detail = {
                k: (v[0] if isinstance(v, list) else v)
                for k, v in detail.items()
            }

        elif isinstance(detail, dict) and "detail" in detail:
            detail = detail["detail"]

        else:
            detail = str(detail)

        response.data = {
            "status": "error",
            "code": getattr(exc, "default_code", "error"),
            "detail": detail,
        }

        return response

    return Response(
        {
            "status": "error",
            "code": "internal_server_error",
            "detail": "Ocurrió un error inesperado en el servidor.",
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
