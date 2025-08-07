import whisper
import speech_recognition as sr
import tempfile
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import base64
import wave
import numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class VoiceChatAPI:
    def __init__(self):
        # Khởi tạo Whisper model
        self.whisper_model = whisper.load_model('base')
        # Khởi tạo speech recognizer
        self.recognizer = sr.Recognizer()
    
    def record_audio_from_mic(self, duration=5):
        """
        Thu âm từ microphone
        """
        try:
            with sr.Microphone() as source:
                print("Đang thu âm...")
                # Điều chỉnh noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Thu âm
                audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
                return audio
        except Exception as e:
            print(f"Lỗi khi thu âm: {e}")
            return None
    
    def save_audio_to_file(self, audio, filename="temp_audio.wav"):
        """
        Lưu audio data vào file
        """
        try:
            with open(filename, "wb") as f:
                f.write(audio.get_wav_data())
            return filename
        except Exception as e:
            print(f"Lỗi khi lưu file audio: {e}")
            return None
    
    def transcribe_with_whisper(self, audio_file_path):
        """
        Chuyển đổi audio thành text bằng Whisper
        """
        try:
            # Load và transcribe audio
            result = self.whisper_model.transcribe(audio_file_path)
            return {
                'success': True,
                'text': result['text'],
                'language': result.get('language', 'unknown')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def transcribe_with_google(self, audio):
        """
        Chuyển đổi audio thành text bằng Google Speech Recognition
        """
        try:
            text = self.recognizer.recognize_google(audio, language='vi-VN')
            return {
                'success': True,
                'text': text,
                'language': 'vi-VN'
            }
        except sr.UnknownValueError:
            return {
                'success': False,
                'error': 'Không thể nhận diện giọng nói'
            }
        except sr.RequestError as e:
            return {
                'success': False,
                'error': f'Lỗi kết nối Google API: {e}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# Khởi tạo instance
voice_chat = VoiceChatAPI()





