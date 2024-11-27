from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from .models import pdf
from .utils import extract_text_from_pdf, generate_gemini_ai_summary

# Create your views here.

def home(request):
    return render(request, 'home.html')

def home2(request):
    return render(request, 'home2.html')

def file_upload(request):
    print(request.FILES)

    if request.method == "POST":
        my_file = request.FILES.get("file")
        uploaded_pdf = pdf.objects.create(file=my_file)
        print("Uploaded file:", my_file.name) 

        text = extract_text_from_pdf(my_file)
        print("Extracted text:", text)

        gemini_response = generate_gemini_ai_summary(text)
        print("Gemini AI response:", gemini_response.text)
        
        return HttpResponse("uploaded")

    return JsonResponse({"post": "false"})

class MainPageView(TemplateView):
    template_name = "home.html"