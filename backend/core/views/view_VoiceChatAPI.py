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


@api_view(['POST'])
@csrf_exempt
def record_and_transcribe(request):
    """
    API endpoint để thu âm và chuyển đổi thành text
    """
    try:
        data = json.loads(request.body)
        duration = data.get('duration', 5)  # Thời gian thu âm (giây)
        use_whisper = data.get('use_whisper', True)  # Sử dụng Whisper hay Google STT
        
        # Thu âm từ microphone
        audio = voice_chat.record_audio_from_mic(duration)
        
        if audio is None:
            return Response({
                'success': False,
                'error': 'Không thể thu âm từ microphone'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Chuyển đổi thành text
        if use_whisper:
            # Lưu audio vào file tạm
            temp_file = voice_chat.save_audio_to_file(audio)
            if temp_file:
                result = voice_chat.transcribe_with_whisper(temp_file)
                # Xóa file tạm
                os.remove(temp_file)
            else:
                result = {'success': False, 'error': 'Không thể lưu file audio'}
        else:
            result = voice_chat.transcribe_with_google(audio)
        
        return Response(result)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def transcribe_audio_file(request):
    """
    API endpoint để chuyển đổi file audio thành text
    """
    try:
        if 'audio_file' not in request.FILES:
            return Response({
                'success': False,
                'error': 'Không tìm thấy file audio'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        audio_file = request.FILES['audio_file']
        use_whisper = request.POST.get('use_whisper', 'true').lower() == 'true'
        
        # Lưu file tạm
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            for chunk in audio_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        
        try:
            if use_whisper:
                result = voice_chat.transcribe_with_whisper(temp_file_path)
            else:
                # Đọc file audio cho Google STT
                with sr.AudioFile(temp_file_path) as source:
                    audio = voice_chat.recognizer.record(source)
                result = voice_chat.transcribe_with_google(audio)
        finally:
            # Xóa file tạm
            os.remove(temp_file_path)
        
        return Response(result)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def transcribe_base64_audio(request):
    """
    API endpoint để chuyển đổi base64 audio thành text
    """
    try:
        data = json.loads(request.body)
        audio_base64 = data.get('audio_base64')
        use_whisper = data.get('use_whisper', True)
        
        if not audio_base64:
            return Response({
                'success': False,
                'error': 'Không tìm thấy audio data'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Decode base64
        audio_data = base64.b64decode(audio_base64)
        
        # Lưu vào file tạm
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
        
        try:
            if use_whisper:
                result = voice_chat.transcribe_with_whisper(temp_file_path)
            else:
                # Đọc file audio cho Google STT
                with sr.AudioFile(temp_file_path) as source:
                    audio = voice_chat.recognizer.record(source)
                result = voice_chat.transcribe_with_google(audio)
        finally:
            # Xóa file tạm
            os.remove(temp_file_path)
        
        return Response(result)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


