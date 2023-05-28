from django.http import HttpResponseBadRequest


class CNPJRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_paths = ["/api/docs/", "/api/schema/"]

        if request.path.startswith("/api/") and request.path not in excluded_paths:
            cnpj = request.headers.get("x-company-cnpj")
            if not cnpj:
                return HttpResponseBadRequest("CNPJ is required in the request headers.")

        response = self.get_response(request)
        return response
