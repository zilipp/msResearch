from django.http import HttpResponse

from core_alg import get_result


def index(request):
    if request.method == 'POST':
        result = get_result.compute()
        return HttpResponse(result)
