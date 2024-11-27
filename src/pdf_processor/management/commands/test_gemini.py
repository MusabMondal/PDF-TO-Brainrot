from django.core.management.base import BaseCommand

from decouple import config
import google.generativeai as genai

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        GEMINI_API_KEY = config("GEMINI_API_KEY", default=None, cast=str)

        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("What is the temperature outside in the GTA?" )

        output = {
            "text": response.text,
            "tokens_used": response.usage_metadata.total_token_count
        }
        print(output)