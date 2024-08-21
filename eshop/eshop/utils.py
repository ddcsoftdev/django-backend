from rest_framework.response import Response
from rest_framework import status


def build_response(status, message=None, data=None) -> Response:
    """Builds and returns a standard response format."""
    response_data = {"status": status}
    if message:
        response_data["message"] = message
    if data:
        response_data["data"] = data
    return Response(response_data, status=status)


def handle_request(service_method) -> Response:
    """Handles exceptions for the service methods."""
    try:
        return service_method()
    except Exception as err:
        return build_response(status=status.HTTP_400_BAD_REQUEST, message=str(err))


def is_user_authorized(request, only_admin: bool = False) -> Response | None:
    """Checks that customers access only their own content, or restricts to admin"""
    auth_user = request.user
    profile = request.data.get("user", None)
    user = profile.get("user", None) if profile else None
    if not auth_user.is_staff or not auth_user.is_superuser:
        if only_admin:
            return build_response(
                status.HTTP_401_UNAUTHORIZED, message="Only admin access"
            )
        elif user["username"] != auth_user.username:
            return build_response(
                status.HTTP_401_UNAUTHORIZED, message="Can only access self data"
            )
    return None
