from django.shortcuts import render
from django.http import HttpResponse

from core_alg import get_result


def index(request):
    result = get_result.compute()
    return HttpResponse(result)
