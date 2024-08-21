from rest_framework.response import Response
from rest_framework import status


def build_response(status: int, message: str = None, data: dict = None) -> Response:
    """Builds and returns a standard API response format."""
    response_data = {"status": status}
    
    if message:
        response_data["message"] = message
    
    if data:
        response_data["data"] = data
    
    return Response(response_data, status=status)


def handle_request(service_method) -> Response:
    """Handles service method execution and catches exceptions."""
    try:
        return service_method()
    except Exception as err:
        return build_response(
            status_code=status.HTTP_400_BAD_REQUEST, 
            message=str(err)
        )
