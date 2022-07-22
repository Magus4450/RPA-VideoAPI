
from rest_framework import generics
from rest_framework.decorators import api_view
from . import serializers
from .handlers import CustomFileUploadHandler
from .models import UploadingVideos, Video
from rest_framework.response import Response


"""
    Class for uploading videos
"""
class VideoCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.VideoSerializer


    def post(self, request, *args, **kwargs):
        
        # Setting custom upload handler
        request.upload_handlers = [CustomFileUploadHandler()]

        return super().post(request, *args, **kwargs)

"""
    Class for getting all videos
"""
class VideoListAPIView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = serializers.VideoSerializer


"""
    View for getting all videos within a size range
"""
@api_view(http_method_names=['GET'])
def SizeVideoListAPIVIew(request, minm = 0, maxm = 1024*1024*1024): # In Bytes
    videos = Video.objects.filter(size_bytes__gte=minm, size_bytes__lte=maxm)
    
    serializer = serializers.VideoSerializer(videos, many=True)
    return Response(serializer.data)


"""
    View for getting all videos from given date to now
"""
@api_view(http_method_names=['GET'])
def DateVideoListAPIVIew(request, date):
    videos = Video.objects.filter(date_uploaded__gte=date)
    serializer = serializers.VideoSerializer(videos, many=True)
    return Response(serializer.data)


"""
    View for getting all videos in size range
"""
@api_view(http_method_names=['GET'])
def LengthVideoListAPIVIew(request, minm, maxm):
    videos = Video.objects.filter(duration_seconds__gte=minm, duration_seconds__lte=maxm)
    serializer = serializers.VideoSerializer(videos, many=True)
    return Response(serializer.data)

"""
    View for getting vidoes that are currently being uploaded
"""
class VideoUploadingListAPIView(generics.ListAPIView):
    serializer_class = serializers.UploadingVideoSerializer

    # Get all vidoes that are currently uploading
    queryset = UploadingVideos.objects.filter(completed=False)


    def list(self, request, *args, **kwargs):
        # Getting original response from the super class
        response =  super().list(request, *args, **kwargs)

        # If no vidoes being uploaded
        if (response.data == []):
            response.data = {"message": "No videos are uploading"}
        
        return response

"""
    View for getting charge of a video given size, length and type of video
"""
@api_view(http_method_names=['GET'])
def VideoChargesAPIVIEW(request, size_bytes, length_seconds, video_type):

    if (length_seconds / 60) > 10:
        return Response({"message": "Video length cannot be more than 10 minutes"}, 400)
    if video_type not in ['mp4', 'mkv']:
        return Response({"message": "video_type must be mp4 or mkv"}, status = 400)

    size_MB = size_bytes / (1024 * 1024)
    
    if(size_MB > 1024):
        return Response({"message": "Video size cannot be more than 1GB"}, status = 400)

    length_min = length_seconds // 60
    length_sec = length_seconds % 60


    charge = 0
    print(size_MB)
    if size_MB < 500:
        charge += 5
    else:
        charge += 12.5

    if length_min < 6 and length_sec < 18:
        charge += 12.5
    else:
        charge += 20


    return Response({
        "charge": "$"+str(charge),
    }, 200)

