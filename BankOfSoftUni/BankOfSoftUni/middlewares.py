from django.http import QueryDict

from BankOfSoftUni.auth_app.views import internal_error


def handle_exceptions_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        context = {}
        if 400 <= response.status_code < 500:
            context['error'] = f'{response.status_code}: {response.reason_phrase}'
            return internal_error(request, context)
        elif response.status_code == 500:
            if request.method == 'GET':
                for form_input_field in QueryDict.dict(request.GET):
                    searched_value = request.GET.get(f'{form_input_field}')
                    search_by = form_input_field
                    if 'customer-search' in request.path or 'targets/search' in request.path:
                        context['error'] = f'No data found for {search_by} "{searched_value}"' \
                                           f'. Please try a different search'
                        return internal_error(request, context)

        elif response.status_code > 500:
            context['error'] = 'System error. Please contact administrator'
            return internal_error(request, context)

        return response

    return middleware
