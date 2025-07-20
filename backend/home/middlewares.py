from django.http import HttpResponseForbidden


class CustomPermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self.has_custom_permission(request.user):
            return HttpResponseForbidden("You do not have permission to access this resource.")
        
        response = self.get_response(request)
        return response

    def has_custom_permission(self, user):
        return user.is_authenticated and user.is_staff