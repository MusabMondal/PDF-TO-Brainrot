import PyPDF2
import google.generativeai as genai
from decouple import config

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    text = ""

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    return text

def generate_gemini_ai_summary(text):
    GEMINI_API_KEY = config("GEMINI_API_KEY", default=None, cast=str)

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Can you summarize the following: " + text)
    
    return response