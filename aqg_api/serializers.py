from rest_framework import serializers
from .models import Document
import os

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'topic', 'file', 'file_type', 'uploaded_at']
        read_only_fields = ['id', 'file_type', 'uploaded_at']
    
    def validate_file(self, value):
        # Check file extension
        ext = os.path.splitext(value.name)[1].lower()
        valid_extensions = ['.pdf', '.docx', '.pptx']
        
        if ext not in valid_extensions:
            raise serializers.ValidationError('Unsupported file type. Please upload PDF, DOCX, or PPTX files.')
        
        # Set file_type based on extension
        if ext == '.pdf':
            self.context['file_type'] = 'pdf'
        elif ext == '.docx':
            self.context['file_type'] = 'docx'
        elif ext == '.pptx':
            self.context['file_type'] = 'pptx'
        
        return value
    
    def create(self, validated_data):
        # Add file_type to validated_data
        validated_data['file_type'] = self.context.get('file_type')
        return super().create(validated_data)