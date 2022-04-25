from django.http import QueryDict

from BankOfSoftUni.auth_app.views import internal_error


def handle_exceptions_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        context = {}
        if response.status_code == 500:
            if 'customer-search' in request.path:
                for form_input_field in QueryDict.dict(request.GET):
                    search_by = form_input_field
                    context['error'] = f'Customer does not exist. Please enter a valid {search_by}'
            else:
                context['error'] = 'customer'
            return internal_error(request, context)
        return response

    return middleware
