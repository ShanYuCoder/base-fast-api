from typing import Any

from fastapi.responses import JSONResponse

SUCCESS_MESSAGE = "Success"
DEFAULT_ERROR = "Error"
VALIDATION_ERROR = "Validation Error"
UNAUTHENTICATED = "Unauthenticated"
FORBIDDEN = "Forbidden"
NOT_FOUND = "Not Found"
INTERNAL_SERVER_ERROR = "Internal Server Error"


def success(
    data: Any = None,
    message: str = SUCCESS_MESSAGE,
    code: int = 200,
    meta: dict[str, Any] | None = None,
    trace_id: str | None = None,
) -> dict[str, Any]:
    return {
        "success": True,
        "code": code,
        "message": message,
        "user_message": None,
        "data": data,
        "meta": meta,
        "trace_id": trace_id,
    }


def error(
    code: int,
    error_label: str,
    message: str | None = None,
    errors: Any = None,
    trace_id: str | None = None,
) -> dict[str, Any]:
    return {
        "success": False,
        "code": code,
        "error": error_label,
        "message": message or error_label,
        "user_message": None,
        "errors": errors,
        "trace_id": trace_id,
        "debug": None,
    }


def error_label_from_status(status: int) -> str:
    mapping = {
        401: UNAUTHENTICATED,
        403: FORBIDDEN,
        404: NOT_FOUND,
        422: VALIDATION_ERROR,
        500: INTERNAL_SERVER_ERROR,
    }
    return mapping.get(status, DEFAULT_ERROR)


def json_success(
    data: Any = None,
    message: str = SUCCESS_MESSAGE,
    code: int = 200,
    meta: dict[str, Any] | None = None,
    status_code: int = 200,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=success(data=data, message=message, code=code, meta=meta),
    )


def json_error(
    status_code: int,
    error_label: str,
    message: str | None = None,
    errors: Any = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=error(status_code, error_label, message, errors),
    )
