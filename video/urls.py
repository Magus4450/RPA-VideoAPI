from django.urls import path
from . import views


urlpatterns = [
    path('video/create/', views.VideoCreateAPIView.as_view()),
    path('video/uploading/', views.VideoUploadingListAPIView.as_view()),
    path('video/charges/<int:size_bytes>/<int:length_seconds>/<str:video_type>', views.VideoChargesAPIVIEW),
    path('video/size/<int:minm>/<int:maxm>/', views.SizeVideoListAPIVIew),
    path('video/date/<str:date>/', views.DateVideoListAPIVIew),
    path('video/length/<int:minm>/<int:maxm>/', views.LengthVideoListAPIVIew),
    path('video/all/', views.VideoListAPIView.as_view()),
]