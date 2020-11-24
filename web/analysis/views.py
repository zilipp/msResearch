from django.http import HttpResponse
from rest_framework import status
from .forms import UploadFileForm
import logging
import os
from pathlib import Path


# self defined functions
from core_alg.AutoMeasurement import AutoMeasurement

# root directory
_root_dir = Path(os.path.dirname(os.path.abspath(__file__)))
# cache directory
_cache_dir = os.path.join(_root_dir.parent, 'cache')

logger = logging.getLogger(__name__)

autoMeasurement = AutoMeasurement()


def index(request):
    if request.method == 'GET':
        result = AutoMeasurement.compute()
        return HttpResponse(result)

    elif request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            logging.info("hhh")
            handle_uploaded_file(request.FILES['file'], model=True)
            handle_uploaded_file(request.FILES['mtl'], model=False)
            # logging.info(request.POST.get('bone_type', 'Humur'))
            result = autoMeasurement.compute(request)
            return result
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


def handle_uploaded_file(f, model):
    logger.error(_cache_dir)
    if model:
        cache_file_path = os.path.join(_cache_dir, 'cache.obj')
    else:
        cache_file_path = os.path.join(_cache_dir, 'Model.mtl')
    with open(cache_file_path, 'wb+') as obj_file:
        for chunk in f.chunks():
            obj_file.write(chunk)
