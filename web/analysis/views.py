from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
# from .bone_model import BoneModelForm
from .forms import UploadFileForm

import logging
import os
from pathlib import Path


from core_alg import get_result

_root_dir = Path(os.path.dirname(os.path.abspath(__file__)))
# cache directory
_cache_dir = os.path.join(_root_dir.parent, 'cache')

logger = logging.getLogger(__name__)

parser_classes = [MultiPartParser, FormParser]


def index(request):
    if request.method == 'GET':
        result = get_result.compute()
        return HttpResponse(result)

    # elif request.method == 'POST':
    #     serializer = BoneModelForm(request.POST, request.FILES)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return HttpResponse(status=status.HTTP_200_OK)
    #     else:
    #         return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


def handle_uploaded_file(f):
    logger.error(_cache_dir)
    cache_file_path = os.path.join(_cache_dir, 'cache1.obj')
    with open(cache_file_path, 'wb+') as obj_file:
        for chunk in f.chunks():
            obj_file.write(chunk)
