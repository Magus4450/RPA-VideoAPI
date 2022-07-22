
from rest_framework import generics
from rest_framework.decorators import api_view
from . import serializers
from .handlers import CustomFileUploadHandler
from .models import UploadingVideos, Video
from rest_framework.response import Response


class VideoCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.VideoSerializer

    def create(self, request, *args, **kwargs):
        print("CREATE")
        response = super().create(request, *args, **kwargs)
        return response

    def post(self, request, *args, **kwargs):
        
        # name = request.data["name"]
        # Setting custom upload handler
        request.upload_handlers = [CustomFileUploadHandler()]

        return super().post(request, *args, **kwargs)

class VideoListAPIView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = serializers.VideoSerializer
    
@api_view(http_method_names=['GET'])
def SizeVideoListAPIVIew(request, minm = 0, maxm = 1024*1024*1024): # In Bytes
    print(minm, maxm)
    videos = Video.objects.filter(size_bytes__gte=minm, size_bytes__lte=maxm)
    
    serializer = serializers.VideoSerializer(videos, many=True)
    return Response(serializer.data)

@api_view(http_method_names=['GET'])
def DateVideoListAPIVIew(request, date):
    videos = Video.objects.filter(date_uploaded__gte=date)
    serializer = serializers.VideoSerializer(videos, many=True)
    return Response(serializer.data)

@api_view(http_method_names=['GET'])
def LengthVideoListAPIVIew(request, minm, maxm):
    videos = Video.objects.filter(duration_seconds__gte=minm, duration_seconds__lte=maxm)
    serializer = serializers.VideoSerializer(videos, many=True)
    return Response(serializer.data)

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

@api_view(http_method_names=['POST'])
def VideoChargesAPIVIEW(request):
    data = request.data
    print(request.POST.keys())
    if 'size_bytes' not in data.keys():
        return Response({"message": "size_bytes is required"}, status = 400)
    
    if 'length_seconds' not in data.keys():
        return Response({"message": "video_length is required"}, status = 400)
    
    if 'video_type' not in data.keys():
        return Response({"message": "video_type is required"}, status = 400)

    # If size_bytes is not a number return error
    try:
        size_MB = float(data['size_bytes']) / (1024 * 1024)
    except ValueError:
        return Response({"message": "size_bytes must be a number"}, status = 400)

    # If length_seconds is not a number return error
    try:
        length_min = int(data['length_seconds']) // 60
        length_sec = int(data['length_seconds']) % 60
    except ValueError:
        return Response({"message": "length_seconds must be a number"}, status = 400)

    video_type = data['video_type']

    if video_type not in ['mp4', 'mkv']:
        return Response({"message": "video_type must be mp4 or mkv"}, status = 400)

    charge = 0

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
    })

