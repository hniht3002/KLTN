from django.db import models
import uuid
import os

class Document(models.Model):
    """Model for storing uploaded documents"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    file = models.FileField(upload_to='store/documents/')
    file_type = models.CharField(max_length=10)  # pdf, docx, pptx
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        # Delete the file when the model instance is deleted
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)

class GeneratedQuestion(models.Model):
    """Model for storing generated questions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_text = models.TextField()
    answer = models.TextField()
    topic = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Most recent questions first

    def __str__(self):
        return f"Question: {self.question_text[:50]}..."

