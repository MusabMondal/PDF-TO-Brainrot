import PyPDF2
import google.generativeai as genai
from decouple import config
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
import elevenlabs
import uuid
from django.core.files import File
from django.core.files.storage import default_storage
from io import BytesIO
from moviepy import VideoFileClip, AudioFileClip
import tempfile
import os
import subprocess

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

def text_to_speech(text):
    
    ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY", default=None, cast=str)

    client = ElevenLabs(
        api_key = ELEVEN_LABS_API_KEY
    )

    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB", # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5", # use the turbo model for low latency
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # plays the audio generated
    # elevenlabs.play(response)

    # Create a BytesIO object to hold the audio data in memory
    audio_stream = BytesIO()

    # Write each chunk of audio data to the stream
    for chunk in response:
        if chunk:
            audio_stream.write(chunk)

    # Reset stream position to the beginning
    audio_stream.seek(0)

    file_name = f"{uuid.uuid4()}.mp3"

    # Return the stream for further use
    return File(audio_stream, name=file_name)


class VideoProcessor:

    def __init__(self, video_filePath, audio_filePath, output_file):
        self.video_filePath = video_filePath
        self.audio_filePath = audio_filePath
        self.output_file = output_file
        self.combined_video = None

    def add_audio_to_video(self):
        # Check if the video and audio files exist before processing
        if not os.path.exists(self.video_filePath):
            raise ValueError(f"Video file does not exist at {self.video_filePath}")
        else:
            print("Video file exists")
        if not os.path.exists(self.audio_filePath):
            raise ValueError(f"Audio file does not exist at {self.audio_filePath}")
        else:
            print("Audio file exists")
        
        try:
            video = VideoFileClip(self.video_filePath)
            audio = AudioFileClip(self.audio_filePath)
        except Exception as e:
            raise ValueError(f"Error loading video or audio file: {e}")

        audioduration = audio.duration
        print("Audio duration:", audioduration)
        videoduration = video.duration
        print("Video duration:", videoduration)

        # Ensure the audio doesn't exceed the video's duration (in case it's longer)
        audio_duration_to_use = min(audioduration, videoduration)
        print("Audio duration to use:", audio_duration_to_use)

        # If the audio is longer than the video, trim it
        if audioduration > videoduration:
            video = video.subclipped(0, audio_duration_to_use)
        else:
            video = video.subclipped(0, audio_duration_to_use)

        # Check the video duration after subclipping
        print("Video duration after subclipping:", video.duration)

        # Combine the video and audio
        video.audio = audio

        # Use self.combined_video directly without reloading it
        print("Video duration:", video.duration)

        self.combined_video = video

    def resize_video(self):
        if self.combined_video is not None:
            original_width, original_height = self.combined_video.size

            # Calculate the new dimensions for a 9:16 video (vertical video)
            new_height = original_width * 16 // 9  # height adjusted to 16:9 aspect ratio
            new_width = original_width  # Keep the width the same

            # Resize the video to fit the 9:16 aspect ratio (resize based on width)
            video_resized = self.combined_video.resize(newsize=(new_width, new_height))

            # Optionally, crop the video to ensure it is framed correctly
            video_cropped = video_resized.crop(x_center=video_resized.w / 2, y_center=video_resized.h / 2, width=new_width, height=new_height)

            self.combined_video = video_cropped
        else:
            raise ValueError("Combined video is None. Please add audio to the video first.")

    def get_combined_video(self):
        return self.combined_video
    
    def get_combined_video_as_bytes(self):
        if self.combined_video is not None:
            try:
                # Create a temporary file to save the video
                with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
                    temp_filename = temp_file.name
                    # Write the combined video to this temporary file
                    self.combined_video.write_videofile(temp_filename, codec="libx264", audio_codec="aac")

                # Read the video back from the temporary file as bytes
                with open(temp_filename, "rb") as f:
                    video_bytes = f.read()

                # Optionally, remove the temporary file after reading the bytes
                os.remove(temp_filename)

                return video_bytes
            except Exception as e:
                raise ValueError(f"Error saving combined video as bytes: {e}")
        else:
            raise ValueError("Combined video is None. Please add audio to the video first.")

    def save_combined_video(self):
        if self.combined_video is not None:
            try:
                # Save the combined video to the output file
                print(self.combined_video.duration)
                self.combined_video.write_videofile(self.output_file, codec="libx264", audio_codec="aac")
            except Exception as e:
                raise ValueError(f"Failed to save combined video: {e}")
        else:
            raise ValueError("Combined video is None. Please add audio to the video first.")