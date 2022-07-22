
from django.utils import timezone
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from .models import UploadingVideos


"""
When file size is less than 2.5 MB, it stores the entire file in the memory and writes the file into disk from memory and is vert fast.
"""
# class CustomMemoryFileUploadHandler(MemoryFileUploadHandler):
#     # This method is run when data is coming in a a new file is needed to store it
#     def new_file(self, *args, **kwargs):
#         super().new_file(*args, **kwargs)
    
#     def file_complete(self, file_size):
#         return super().file_complete(file_size) 

#     def handle_raw_input(
#         self, input_data, META, content_length, boundary, encoding=None
#     ):
#         """
#         Use the content_length to signal whether or not this handler should be
#         used.
#         """
#         # Check the content-length header to see if we should
#         # If the post is too large, we cannot use the Memory handler.
#         super().handle_raw_input(input_data, META, content_length, boundary, encoding)
#         # uploading = UploadingVideos.objects.create(
#         #     name = self.filename
#         # )
#         # uploading.save()


"""
If file size is large, it will write uploaded file into a temporary location in system's temp directory
"""

# This class handles all file uploads grated than 2.5MB (Default)
class CustomFileUploadHandler(TemporaryFileUploadHandler):
    
 
    def __init__(self):
        self.uploading = None


    # This method runs when a new file in being created to store the incoming video
    def new_file(self, *args, **kwargs):
        super().new_file(*args, **kwargs)
        
        # Storing name of the video and the current time when the video is being uploaded
        self.uploading = UploadingVideos.objects.create(name=self.file_name, start_time = timezone.now())
        self.uploading.save()
    
    def file_complete(self, file_size):

       
        # Getting the time of completion of video upload
        end_time = timezone.now()

        # Getting total time taken
        self.uploading.end_time = end_time
        self.uploading.time_taken_seconds = (end_time - self.uploading.start_time).total_seconds()

        # Setting completed as True and saving
        self.uploading.completed = True
        self.uploading.save()

        return super().file_complete(file_size) 
