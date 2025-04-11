from django.urls import path
from .views import UploadFileView, GenerateQuestionsView, EvaluateQuestionsView, UploadAndGenerateView

urlpatterns = [
    path('upload/', UploadFileView.as_view(), name='upload_file'),
    path('generate-questions/', GenerateQuestionsView.as_view(), name='generate_questions'),
    path("upload-and-generate/", UploadAndGenerateView.as_view(), name="upload_and_generate"),
    path('evaluate/', EvaluateQuestionsView.as_view(), name='evaluate_questions'),
]