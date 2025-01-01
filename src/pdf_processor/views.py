from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from .models import pdf
from .utils import extract_text_from_pdf, generate_gemini_ai_summary, text_to_speech, VideoProcessor
import os

# Create your views here.

def home(request):
    return render(request, 'home.html')

def home2(request):
    return render(request, 'home2.html')

def file_upload(request):
    print(request.FILES)

    if request.method == "POST":
        my_file = request.FILES.get("file")
        print("Uploaded file:", my_file.name)

        print("Extracting text from PDF...")
        # Extract text from the uploaded PDF
        text = extract_text_from_pdf(my_file)

        print("Generating AI summary...")
        # Generate AI summary for the extracted text
        gemini_response = generate_gemini_ai_summary(text)

        # Create the initial pdf model instance without the audio file
        uploaded_pdf = pdf.objects.create(
            file=my_file,  # The uploaded PDF file
            summary=gemini_response.text,  # AI-generated summary
            text=text  # Extracted text from PDF
        )

        print("Generating audio file...")
        # Generate the audio file from the summary text
        audio_file = text_to_speech(gemini_response.text)

        # Save the audio file to the pdf instance
        uploaded_pdf.audio = audio_file  # Assign the audio file
        uploaded_pdf.save()  # Save the model instance with the audio file

        audio_fileName = audio_file.name

        print("Audio file saved:", audio_fileName)

        print(os.getcwd())

        audio_filePath = f"C:\\Users\\musab\\OneDrive\\Documents\\Projects\\brainrot_learning\\brainrotlearning\\src\\media\\audios\\{audio_file.name}"

        video_filePath = f"C:\\Users\\musab\\OneDrive\\Documents\\Projects\\brainrot_learning\\brainrotlearning\\src\\media\\videos\\Minecraft_Parkour_gameplay_tiktok_format_9_16.mp4"



        print("Adding audio to video...")
        videoProcessor = VideoProcessor(video_filePath,audio_filePath, f"media/videos/{my_file.name.split('.')[0]}_output.mp4")
        videoProcessor.add_audio_to_video()
        print("Saving combined video...")
        videoProcessor.save_combined_video()

        return HttpResponse("File uploaded and audio saved.")

    return JsonResponse({"post": "false"})

class MainPageView(TemplateView):
    template_name = "home.html"