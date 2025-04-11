from django.shortcuts import render
# Create your views here.
def upload_document_page(request):
    return render(request, 'aqg/upload_files.html')

def gene_questions_page(request):
    return render(request, 'aqg/gene_questions.html')

def evaluate_questions(request):
    return render(request, 'aqg/evaluate_questions.html')
