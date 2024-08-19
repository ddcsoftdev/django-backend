from rest_framework.response import Response

def build_response(status_code, message=None, data=None) -> Response:
    """Builds and returns a standard response format."""
    response_data = {"status": status_code}
    if message:
        response_data["message"] = message
    if data:
        response_data["data"] = data
    return Response(response_data, status=status_code)