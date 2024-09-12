from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UploadedFile
import uuid
from admin.decorator import api_key_required
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from moviepy.editor import VideoFileClip
import os
from django.core.files import File  # Import Django's File class


# Path to store the compressed files temporarily
TEMP_COMPRESSED_DIR = 'tmp/'  # Update this path to an appropriate location

@api_view(['POST'])
@api_key_required
@csrf_exempt
def upload_files(request):
    base_url = request.get_host()
    if 'file' not in request.FILES:
        return Response({'error': 'No file(s) provided'}, status=status.HTTP_400_BAD_REQUEST)

    file_urls = []

    # Loop through each file in the request
    for file in request.FILES.getlist('file'):
        random_name = str(uuid.uuid4()) + '_' + file.name
        file_extension = file.name.split('.')[-1].lower()

        if file.content_type.startswith('image/'):
            # Compress image to 60% quality
            compressed_image_path = compress_image(file, random_name)
            file_url = save_file_to_db(compressed_image_path, base_url, file)
        elif file.content_type.startswith('video/'):
            # Compress video to 720p and 30 FPS
            compressed_video_path = compress_video(file, random_name)
            file_url = save_file_to_db(compressed_video_path, base_url, file)
        else:
            # If not an image or video, just save it as is
            uploaded_file = UploadedFile(file=file)
            uploaded_file.save()
            file_url = "http://" + base_url + uploaded_file.file.url
        
        file_urls.append(file_url)

    return Response({'file_urls': file_urls}, status=status.HTTP_201_CREATED)


def compress_image(image_file, random_name):
    """Compress image using Pillow to 60% quality."""
    img = Image.open(image_file)
    print("Compressing Image....")
    compressed_image_path = os.path.join(TEMP_COMPRESSED_DIR, random_name)
    
    # Save the image with 60% quality
    img.save(compressed_image_path, optimize=True, quality=50)
    
    return compressed_image_path


def compress_video(video_file, random_name):
    """Compress video using MoviePy to 720p resolution and 30 FPS."""
    video_clip = VideoFileClip(video_file.temporary_file_path())
    compressed_video_path = os.path.join(TEMP_COMPRESSED_DIR, random_name)

    # Resize to 720p (1280x720) and set frame rate to 30 FPS
    video_clip = video_clip.resize((1280, 720)).set_fps(30)
    
    # Write the video with 720p, 30 FPS, and compress it (adjusting bitrate if needed)
    video_clip.write_videofile(compressed_video_path, bitrate='500k', preset='medium')
    
    return compressed_video_path


def save_file_to_db(compressed_file_path, base_url, original_file):
    """Save the compressed file to the database."""
    with open(compressed_file_path, 'rb') as f:
        # Wrap the file in Django's File object
        django_file = File(f)
        uploaded_file = UploadedFile(file=django_file)
        uploaded_file.save()

    file_path = uploaded_file.file.url
    file_url = "http://" + base_url + file_path

    # Optionally, delete the compressed file after saving to avoid consuming disk space
    os.remove(compressed_file_path)

    return file_url
