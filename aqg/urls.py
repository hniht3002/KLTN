from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_document_page, name="upload_document_page"),
    path("generate-questions/", views.gene_questions_page, name="gene_questions_page"),
    path("evaluate/", views.evaluate_questions, name="evaluate_questions"),
]