
from rest_framework import serializers
from .models import Video, UploadingVideos
from moviepy.editor import VideoFileClip

from django.utils import timezone
class VideoSerializer(serializers.ModelSerializer):


    video = serializers.FileField(
        required = True,
    )
    class Meta:
        model = Video
        fields = ('video', 'duration_seconds', 'size_bytes', 'date_uploaded')


    def validate(self, attrs):

        video  = attrs['video']
        size_bytes = video.size

        # Name of file stored in temporary buffer -> TemporaryUploadedFile
        temp_video_name = video.file.name

        # Checking file type
        filetype = temp_video_name.split(".")[-1]
        if filetype not in ["mp4", "mkv"]:
            raise serializers.ValidationError("Only mp4 and mkv videos are allowed")

        # Using VideoFileClip to get duration of video
        video_file = VideoFileClip(video.file.name)
        seconds = video_file.duration

        # Checking if video is less than 10 minutes
        if seconds > 600:
            raise serializers.ValidationError("Video cannot exceed length of 10 minutes")

        if size_bytes > (1 * 1024 * 1024 * 1024):
            raise serializers.ValidationError("Video cannot exceed 1GB")

        # Storing the data in attrs to be used in other methods
        attrs["duration_seconds"] = seconds
        attrs["size_bytes"] = size_bytes
        return super().validate(attrs)


    def create(self, validated_data):
        video = Video.objects.create(
            duration_seconds = validated_data["duration_seconds"],
            size_bytes = validated_data["size_bytes"],
            date_uploaded = timezone.now(),
            video = validated_data["video"],
        )
        return video

class UploadingVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadingVideos
        fields = ('name' , 'start_time')