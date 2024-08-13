from flask import current_app as app
from service.models import DataValidationError
from service import api
from . import status  # pylint: disable=E0611
from werkzeug.exceptions import (
    NotFound,
    MethodNotAllowed,
    UnsupportedMediaType,
)

######################################################################
# Error Handlers
######################################################################


@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """Handles Value Errors from bad data"""
    message = str(error)
    app.logger.error(message)
    return {
        "status": status.HTTP_400_BAD_REQUEST,
        "error": "Bad Request",
        "message": message,
    }, status.HTTP_400_BAD_REQUEST


@api.errorhandler(NotFound)
def not_found_error(error):
    """Handles resources not found with 404_NOT_FOUND"""
    message = str(error)
    app.logger.warning(message)
    return {
        "status": status.HTTP_404_NOT_FOUND,
        "error": "Not Found",
        "message": message,
    }, status.HTTP_404_NOT_FOUND


@api.errorhandler(MethodNotAllowed)
def method_not_allowed_error(error):
    """Handles unsupported HTTP methods with 405_METHOD_NOT_ALLOWED"""
    message = str(error)
    app.logger.warning(message)
    return {
        "status": status.HTTP_405_METHOD_NOT_ALLOWED,
        "error": "Method Not Allowed",
        "message": message,
    }, status.HTTP_405_METHOD_NOT_ALLOWED


@api.errorhandler(UnsupportedMediaType)
def unsupported_media_type_error(error):
    """Handles unsupported media requests with 415_UNSUPPORTED_MEDIA_TYPE"""
    message = str(error)
    app.logger.warning(message)
    return {
        "status": status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "error": "Unsupported Media Type",
        "message": message,
    }, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


# @api.errorhandler(InternalServerError)
# def internal_server_error(error):
#     """Handles unexpected server error with 500_SERVER_ERROR"""
#     message = str(error)
#     app.logger.error(message)
#     return {
#         "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
#         "error": "Internal Server Error",
#         "message": message,
#     }, status.HTTP_500_INTERNAL_SERVER_ERROR


# @api.errorhandler(Exception)
# def handle_unexpected_error(error):
#     """Handles any unexpected errors"""
#     message = str(error)
#     app.logger.error(f"Unexpected error: {message}")
#     return {
#         "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
#         "error": "Internal Server Error",
#         "message": "An unexpected error occurred.",
#     }, status.HTTP_500_INTERNAL_SERVER_ERROR
