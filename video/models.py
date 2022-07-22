from django.db import models


class Video(models.Model):

    # name = models.CharField(max_length=200)
    duration_seconds = models.IntegerField(null=True, blank=True)
    size_bytes = models.IntegerField(null=True, blank=True)
    date_uploaded = models.DateTimeField(null=True, blank=True)
    video = models.FileField(upload_to='video/')

    def __str__(self) :
        return self.name


class UploadingVideos(models.Model):
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    time_taken_seconds = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
