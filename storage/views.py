from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UploadedFile
from .serializers import UploadedFileSerializer
import uuid
from admin.decorator import api_key_required
from django.views.decorators.csrf import csrf_exempt




@api_view(['POST'])
@api_key_required
@csrf_exempt
def upload_file(request):
    base_url = request.get_host()
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']
    random_name = str(uuid.uuid4()) + '_' + file.name
    uploaded_file = UploadedFile(file=file)
    uploaded_file.save()
    file_path = uploaded_file.file.url
    file_url = "http://"+ base_url + file_path
    return Response({'file_url': file_url}, status=status.HTTP_201_CREATED)
