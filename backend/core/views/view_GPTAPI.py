import openai
import json
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import os
from core.models.CapDo import CapDo
from core.models.ChuDe import ChuDe
import hashlib
from django.core.cache import cache
from datetime import datetime, timedelta
import time
import logging
import uuid
import tempfile

# Import gTTS cho Text-to-Speech
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    logging.warning("gTTS not available. Install with: pip install gtts")

# Import models để lấy dữ liệu từ database
from core.models import ChuDe, CapDo, NgonNgu

# Cấu hình logging
logger = logging.getLogger(__name__)

# Cấu hình OpenAI API
openai.api_key = settings.OPENAI_API_KEY

class GPTAPI:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.cache_timeout = 7200  # Cache 2 giờ để tiết kiệm API calls
        self.rate_limit_per_minute = 10  # Giảm xuống 5 requests/phút/user
        self.rate_limit_per_hour = 100   # Giảm xuống 50 requests/giờ/user
        self.max_retries = 3
        self.retry_delay = 2  # seconds
        
        # Fallback responses cho các câu hỏi phổ biến
        self.fallback_responses = {
            "hello": "Xin chào! Tôi là trợ lý AI học tập. Tôi có thể giúp bạn học tập và trả lời các câu hỏi. Hiện tại tôi đang gặp một chút vấn đề kỹ thuật, nhưng tôi vẫn có thể hỗ trợ bạn!",
            "help": "Tôi có thể giúp bạn:\n- Trả lời câu hỏi học tập\n- Giải thích khái niệm\n- Đưa ra gợi ý học tập\n- Hỗ trợ luyện tập\n\nHãy hỏi tôi bất kỳ điều gì!",
            "error": "Xin lỗi, hiện tại tôi đang gặp vấn đề kỹ thuật. Vui lòng thử lại sau hoặc liên hệ admin để được hỗ trợ.",
            "quota_exceeded": "Xin lỗi, hiện tại hệ thống đã đạt giới hạn sử dụng. Vui lòng thử lại sau ít phút hoặc liên hệ admin để được hỗ trợ thêm."
        }
    
    def check_api_key_validity(self):
        """
        Kiểm tra API key có hợp lệ không
        """
        try:
            # Thử gọi API đơn giản để kiểm tra
            response = self.client.models.list()
            return True
        except Exception as e:
            logger.error(f"API key validation failed: {e}")
            return False
    
    def get_topic_from_database(self, topic_id=None, topic_name=None):
        """
        Lấy thông tin chủ đề từ database
        """
        try:
            if topic_id:
                return ChuDe.objects.get(id=topic_id)
            elif topic_name:
                return ChuDe.objects.get(ten_chu_de__icontains=topic_name)
            else:
                return None
        except ChuDe.DoesNotExist:
            return None
    
    def get_level_from_database(self, level_id=None, level_name=None):
        """
        Lấy thông tin cấp độ từ database
        """
        try:
            if level_id:
                return CapDo.objects.get(id=level_id)
            elif level_name:
                return CapDo.objects.get(ten_cap_do__icontains=level_name)
            else:
                return None
        except CapDo.DoesNotExist:
            return None
    
    def get_all_topics(self):
        """
        Lấy tất cả chủ đề từ database
        """
        try:
            return ChuDe.objects.all()
        except Exception as e:
            logger.error(f"Error getting topics: {e}")
            return []
    
    def get_all_levels(self):
        """
        Lấy tất cả cấp độ từ database
        """
        try:
            return CapDo.objects.all()
        except Exception as e:
            logger.error(f"Error getting levels: {e}")
            return []
    
    def check_rate_limit(self, user_id=None):
        """
        Kiểm tra rate limit để bảo vệ Student Plan
        """
        if not user_id:
            user_id = "anonymous"
        
        now = datetime.now()
        minute_key = f"rate_limit_minute_{user_id}_{now.strftime('%Y%m%d%H%M')}"
        hour_key = f"rate_limit_hour_{user_id}_{now.strftime('%Y%m%d%H')}"
        
        # Kiểm tra giới hạn phút
        minute_count = cache.get(minute_key, 0)
        if minute_count >= self.rate_limit_per_minute:
            return False, "Quá nhiều requests trong 1 phút. Vui lòng thử lại sau."
        
        # Kiểm tra giới hạn giờ
        hour_count = cache.get(hour_key, 0)
        if hour_count >= self.rate_limit_per_hour:
            return False, "Quá nhiều requests trong 1 giờ. Vui lòng thử lại sau."
        
        # Tăng counter
        cache.set(minute_key, minute_count + 1, 60)
        cache.set(hour_key, hour_count + 1, 3600)
        
        return True, None
    
    def create_cache_key(self, user_message, topic=None, level=None):
        """
        Tạo cache key để lưu trữ response
        """
        content = f"{user_message}_{topic}_{level}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get_cached_response(self, cache_key):
        """
        Lấy response từ cache nếu có
        """
        return cache.get(f"gpt_response_{cache_key}")
    
    def set_cached_response(self, cache_key, response):
        """
        Lưu response vào cache
        """
        cache.set(f"gpt_response_{cache_key}", response, self.cache_timeout)
    
    def get_fallback_response(self, user_message):
        """
        Trả về fallback response khi OpenAI không khả dụng
        """
        user_message_lower = user_message.lower()
        
        # Kiểm tra các từ khóa phổ biến
        if any(word in user_message_lower for word in ['xin chào', 'hello', 'hi', 'chào']):
            return self.fallback_responses["hello"]
        elif any(word in user_message_lower for word in ['giúp', 'help', 'hỗ trợ']):
            return self.fallback_responses["help"]
        elif any(word in user_message_lower for word in ['lỗi', 'error', 'không hoạt động']):
            return self.fallback_responses["error"]
        else:
            # Trả về response chung
            return f"Xin lỗi, hiện tại tôi đang gặp vấn đề kỹ thuật. Tôi hiểu bạn đang hỏi về: '{user_message}'. Vui lòng thử lại sau hoặc liên hệ admin để được hỗ trợ."
    
    def create_learning_prompt(self, user_message, topic=None, level=None):
        """
        Tạo prompt ngắn gọn để tiết kiệm token
        """
        prompt = f"Trả lời: {user_message}"
        
        if topic:
            if isinstance(topic, ChuDe):
                prompt += f" (Chủ đề: {topic.ten_chu_de})"
            else:
                prompt += f" (Chủ đề: {topic})"
        
        if level:
            if isinstance(level, CapDo):
                prompt += f" (Trình độ: {level.ten_cap_do})"
            else:
                level_map = {
                    'beginner': 'sơ cấp',
                    'intermediate': 'trung cấp', 
                    'advanced': 'cao cấp'
                }
                prompt += f" (Trình độ: {level_map.get(level, level)})"
        
        prompt += ". Trả lời ngắn gọn, thân thiện."
        
        return prompt
    
    def call_openai_api(self, prompt, retry_count=0):
        """
        Gọi OpenAI API với retry mechanism
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Model rẻ nhất cho Student Plan
                messages=[
                    {"role": "system", "content": "Bạn là trợ lý AI giảng dạy thân thiện. Trả lời ngắn gọn, dễ hiểu."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,  # Giảm token để tiết kiệm chi phí
                temperature=0.3,  # Giảm temperature để ổn định và tiết kiệm
                top_p=0.8,
                frequency_penalty=0,
                presence_penalty=0
            )
            return {
                'success': True,
                'response': response.choices[0].message.content.strip(),
                'model': response.model,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens,
                    'cached': False
                }
            }
        except openai.RateLimitError as e:
            logger.error(f"Rate limit error: {e}")
            if retry_count < self.max_retries:
                time.sleep(self.retry_delay * (retry_count + 1))
                return self.call_openai_api(prompt, retry_count + 1)
            else:
                return {
                    'success': False,
                    'error': 'Rate limit exceeded',
                    'message': 'Quá nhiều requests. Vui lòng thử lại sau.'
                }
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            if "insufficient_quota" in str(e) or "quota" in str(e):
                return {
                    'success': False,
                    'error': 'insufficient_quota',
                    'message': 'API quota exceeded. Using fallback response.'
                }
            else:
                return {
                    'success': False,
                    'error': 'api_error',
                    'message': f'OpenAI API error: {str(e)}'
                }
                
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                'success': False,
                'error': 'unexpected_error',
                'message': f'Unexpected error: {str(e)}'
            }
    
    def get_gpt_response(self, user_message, topic_id=None, level_id=None, topic_name=None, level_name=None):
        """
        Gửi tin nhắn lên GPT và nhận phản hồi - Tối ưu cho Student Plan
        """
        try:
            # Lấy thông tin topic và level từ database
            topic = None
            level = None
            
            if topic_id or topic_name:
                topic = self.get_topic_from_database(topic_id, topic_name)
            
            if level_id or level_name:
                level = self.get_level_from_database(level_id, level_name)
            
            # Tạo cache key với thông tin từ database
            topic_str = topic.ten_chu_de if topic else None
            level_str = level.ten_cap_do if level else None
            cache_key = self.create_cache_key(user_message, topic_str, level_str)
            
            # Kiểm tra cache trước
            cached_response = self.get_cached_response(cache_key)
            if cached_response:
                logger.info("Using cached response - saving API cost")
                return {
                    'success': True,
                    'response': cached_response,
                    'model': 'gpt-3.5-turbo (cached)',
                    'usage': {
                        'prompt_tokens': 0,
                        'completion_tokens': 0,
                        'total_tokens': 0,
                        'cached': True
                    },
                    'topic': {
                        'id': topic.id if topic else None,
                        'name': topic.ten_chu_de if topic else None,
                        'language': topic.ngon_ngu.ten_ngon_ngu if topic else None
                    } if topic else None,
                    'level': {
                        'id': level.id if level else None,
                        'name': level.ten_cap_do if level else None
                    } if level else None
                }
            # Kiểm tra API key validity
            if not self.check_api_key_validity():
                logger.warning("API key invalid, using fallback response")
                fallback_response = self.get_fallback_response(user_message)
                return {
                    'success': True,
                    'response': fallback_response,
                    'model': 'fallback',
                    'usage': {
                        'prompt_tokens': 0,
                        'completion_tokens': 0,
                        'total_tokens': 0,
                        'cached': False,
                        'fallback': True
                    },
                    'topic': {
                        'id': topic.id if topic else None,
                        'name': topic.ten_chu_de if topic else None,
                        'language': topic.ngon_ngu.ten_ngon_ngu if topic else None
                    } if topic else None,
                    'level': {
                        'id': level.id if level else None,
                        'name': level.ten_cap_do if level else None
                    } if level else None
                }
            
            # Gọi OpenAI API
            prompt = self.create_learning_prompt(user_message, topic, level)
            api_result = self.call_openai_api(prompt)
            
            # Xử lý kết quả API
            if api_result['success']:
                response_text = api_result['response']
                # Lưu vào cache để tiết kiệm API calls
                self.set_cached_response(cache_key, response_text)
                
                return {
                    'success': True,
                    'response': response_text,
                    'model': api_result['model'],
                    'usage': api_result['usage'],
                    'topic': {
                        'id': topic.id if topic else None,
                        'name': topic.ten_chu_de if topic else None,
                        'language': topic.ngon_ngu.ten_ngon_ngu if topic else None
                    } if topic else None,
                    'level': {
                        'id': level.id if level else None,
                        'name': level.ten_cap_do if level else None
                    } if level else None
                }
            else:
                # API lỗi, sử dụng fallback
                logger.warning(f"OpenAI API failed: {api_result['error']}")
                fallback_response = self.get_fallback_response(user_message)
                return {
                    'success': True,
                    'response': fallback_response,
                    'model': 'fallback',
                    'usage': {
                        'prompt_tokens': 0,
                        'completion_tokens': 0,
                        'total_tokens': 0,
                        'cached': False,
                        'fallback': True
                    },
                    'api_error': api_result['error'],
                    'topic': {
                        'id': topic.id if topic else None,
                        'name': topic.ten_chu_de if topic else None,
                        'language': topic.ngon_ngu.ten_ngon_ngu if topic else None
                    } if topic else None,
                    'level': {
                        'id': level.id if level else None,
                        'name': level.ten_cap_do if level else None
                    } if level else None
                }
        except Exception as e:
            logger.error(f"Unexpected error in get_gpt_response: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Lỗi hệ thống: ' + str(e)
            }
    
    

# Khởi tạo instance
gpt_api = GPTAPI()
@api_view(['POST'])
@csrf_exempt
def chat_with_gpt(request):
    """
    API endpoint để chat với GPT - Tối ưu cho Student Plan
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        topic_id = data.get('topic_id', None)
        level_id = data.get('level_id', None)
        topic_name = data.get('topic_name', None)
        level_name = data.get('level_name', None)
        
        user_id = data.get('user_id', None)  # Để tracking rate limit
        
        if not user_message:
            return Response({
                'success': False,
                'error': 'Tin nhắn không được để trống'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Kiểm tra rate limit để bảo vệ Student Plan
        rate_ok, rate_error = gpt_api.check_rate_limit(user_id)
        if not rate_ok:
            return Response({
                'success': False,
                'error': rate_error,
                'rate_limited': True,
                'message': 'Vui lòng thử lại sau để tránh vượt quá giới hạn sử dụng.'
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        # Gửi tin nhắn lên GPT
        result = gpt_api.get_gpt_response(
            user_message, 
            topic_id=topic_id, 
            level_id=level_id,
            topic_name=topic_name,
            level_name=level_name
        )
        
        # Thêm thông tin Student Plan và status
        result['student_plan'] = True
        result['cost_saving'] = result.get('usage', {}).get('cached', False)
        
        # Thêm thông tin về API status
        if result.get('usage', {}).get('fallback', False):
            result['api_status'] = 'fallback'
            result['message'] = 'Đang sử dụng chế độ dự phòng do vấn đề kỹ thuật.'
        elif result.get('usage', {}).get('cached', False):
            result['api_status'] = 'cached'
            result['message'] = 'Sử dụng dữ liệu đã lưu để tiết kiệm chi phí.'
        else:
            result['api_status'] = 'live'
            result['message'] = 'Kết nối trực tiếp với OpenAI.'
        
        return Response(result)
        
    except json.JSONDecodeError:
        return Response({
            'success': False,
            'error': 'Dữ liệu JSON không hợp lệ'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        logger.error(f"Error in chat_with_gpt: {e}")
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Lỗi hệ thống, vui lòng thử lại sau.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@csrf_exempt
def get_learning_suggestions(request):
    """
    API endpoint để lấy gợi ý học tập
    """
    try:
        topic_id = request.GET.get('topic_id', None)
        level_id = request.GET.get('level_id', None)
        topic_name = request.GET.get('topic_name', None)
        level_name = request.GET.get('level_name', None)
        
        # Lấy gợi ý học tập
        result = gpt_api.get_learning_suggestions(
            topic_id=topic_id,
            level_id=level_id,
            topic_name=topic_name,
            level_name=level_name
        )
        
        # Thêm thông tin status
        if result.get('fallback', False):
            result['api_status'] = 'fallback'
            result['message'] = 'Đang sử dụng gợi ý dự phòng.'
        else:
            result['api_status'] = 'live'
            result['message'] = 'Gợi ý được tạo bởi AI.'
        
        return Response(result)
        
    except Exception as e:
        logger.error(f"Error in get_learning_suggestions: {e}")
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Không thể lấy gợi ý học tập.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@api_view(['GET'])
@csrf_exempt
def check_api_status(request):
    """
    API endpoint để kiểm tra trạng thái OpenAI API
    """
    try:
        api_valid = gpt_api.check_api_key_validity()
        
        return Response({
            'success': True,
            'api_status': 'valid' if api_valid else 'invalid',
            'message': 'API key hợp lệ.' if api_valid else 'API key không hợp lệ hoặc đã hết quota.',
            'student_plan': True,
            'recommendations': [
                'Sử dụng cache để tiết kiệm API calls',
                'Giới hạn rate limit để tránh vượt quota',
                'Sử dụng fallback responses khi API lỗi'
            ] if api_valid else [
                'Kiểm tra lại API key',
                'Nạp thêm credit cho tài khoản OpenAI',
                'Liên hệ admin để được hỗ trợ'
            ]
        })
        
    except Exception as e:
        logger.error(f"Error in check_api_status: {e}")
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Không thể kiểm tra trạng thái API.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['POST'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tts_gtts(request):
    """
    API endpoint để chuyển text thành giọng nói sử dụng gTTS
    Hỗ trợ authentication để lấy ngôn ngữ từ database
    """
    if not GTTS_AVAILABLE:
        return Response({
            'success': False,
            'error': 'gTTS not available. Install with: pip install gtts'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        lang = data.get('lang', None)
        
        # Hàm chuyển đổi mã ngôn ngữ từ database sang gTTS
        def convert_lang_code_to_gtts(db_code):
            # Mapping từ mã ngôn ngữ trong database sang mã gTTS
            lang_mapping = {
                'vi': 'vi',  # Vietnamese
                'en': 'en',  # English
                'fr': 'fr',  # French
                'de': 'de',  # German
                'es': 'es',  # Spanish
                'it': 'it',  # Italian
                'pt': 'pt',  # Portuguese
                'ru': 'ru',  # Russian
                'ja': 'ja',  # Japanese
                'ko': 'ko',  # Korean
                'zh': 'zh',  # Chinese
                'ar': 'ar',  # Arabic
                'hi': 'hi',  # Hindi
                'th': 'th',  # Thai
                'id': 'id',  # Indonesian
                'ms': 'ms',  # Malay
                'nl': 'nl',  # Dutch
                'sv': 'sv',  # Swedish
                'da': 'da',  # Danish
                'no': 'no',  # Norwegian
                'fi': 'fi',  # Finnish
                'pl': 'pl',  # Polish
                'tr': 'tr',  # Turkish
                'he': 'he',  # Hebrew
                'el': 'el',  # Greek
                'hu': 'hu',  # Hungarian
                'cs': 'cs',  # Czech
                'sk': 'sk',  # Slovak
                'ro': 'ro',  # Romanian
                'bg': 'bg',  # Bulgarian
                'hr': 'hr',  # Croatian
                'sl': 'sl',  # Slovenian
                'et': 'et',  # Estonian
                'lv': 'lv',  # Latvian
                'lt': 'lt',  # Lithuanian
                'mt': 'mt',  # Maltese
                'ga': 'ga',  # Irish
                'cy': 'cy',  # Welsh
                'eu': 'eu',  # Basque
                'ca': 'ca',  # Catalan
                'gl': 'gl',  # Galician
                'is': 'is',  # Icelandic
                'mk': 'mk',  # Macedonian
                'sq': 'sq',  # Albanian
                'sr': 'sr',  # Serbian
                'bs': 'bs',  # Bosnian
                'me': 'me',  # Montenegrin
                'uk': 'uk',  # Ukrainian
                'be': 'be',  # Belarusian
                'kk': 'kk',  # Kazakh
                'ky': 'ky',  # Kyrgyz
                'uz': 'uz',  # Uzbek
                'tg': 'tg',  # Tajik
                'mn': 'mn',  # Mongolian
                'ka': 'ka',  # Georgian
                'hy': 'hy',  # Armenian
                'az': 'az',  # Azerbaijani
                'fa': 'fa',  # Persian
                'ur': 'ur',  # Urdu
                'bn': 'bn',  # Bengali
                'ta': 'ta',  # Tamil
                'te': 'te',  # Telugu
                'ml': 'ml',  # Malayalam
                'kn': 'kn',  # Kannada
                'gu': 'gu',  # Gujarati
                'pa': 'pa',  # Punjabi
                'or': 'or',  # Odia
                'as': 'as',  # Assamese
                'ne': 'ne',  # Nepali
                'si': 'si',  # Sinhala
                'my': 'my',  # Burmese
                'km': 'km',  # Khmer
                'lo': 'lo',  # Lao
            }
            
            # Chuẩn hóa mã ngôn ngữ
            if db_code:
                db_code = db_code.lower().strip()
                
            # Kiểm tra trong mapping
            if db_code in lang_mapping:
                logger.info(f"Found mapping for {db_code}: {lang_mapping[db_code]}")
                return lang_mapping[db_code]
            
            # Nếu không tìm thấy, log và trả về mã gốc
            logger.warning(f"No mapping found for language code: {db_code}, using original code")
            return db_code if db_code else 'vi'
        
        # Nếu không có lang được gửi từ frontend, lấy từ database hồ sơ học tập
        if not lang and request.user.is_authenticated:
            try:
                from core.models.HoSoHocTap import HoSoHocTap
                hoso = HoSoHocTap.objects.filter(khach_hang=request.user).first()
                if hoso and hoso.ngon_ngu_hoc:
                    db_lang_code = hoso.ngon_ngu_hoc.ma_ngon_ngu
                    lang = convert_lang_code_to_gtts(db_lang_code)
                    logger.info(f"Lấy ngôn ngữ từ database: {db_lang_code} -> gTTS: {lang}")
                else:
                    logger.warning(f"Không tìm thấy hồ sơ học tập cho user {request.user.id}")
            except Exception as e:
                logger.error(f"Lỗi khi lấy ngôn ngữ từ database: {e}")
        
        # Log thông tin ngôn ngữ được sử dụng
        logger.info(f"TTS Request - Lang from frontend: {lang}, User: {request.user.id if request.user.is_authenticated else 'Anonymous'}")
        
        # Nếu có lang từ frontend, chuyển đổi qua hàm convert
        if lang:
            original_lang = lang
            lang = convert_lang_code_to_gtts(lang)
            logger.info(f"Language conversion: {original_lang} -> {lang}")
        
        # Fallback về ngôn ngữ từ database hoặc 'vi' nếu không lấy được
        gtts_lang = lang or 'vi'
        logger.info(f"Final gTTS language: {gtts_lang}")
        
        # Debug: Log toàn bộ request data
        logger.info(f"TTS Request Data: {data}")
        logger.info(f"TTS Request Headers: {dict(request.headers)}")
        
        if not text:
            return Response({
                'success': False,
                'error': 'Text không được để trống'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Tạo file audio tạm thời - tương thích với Windows
        import tempfile
        temp_dir = tempfile.gettempdir()
        filename = os.path.join(temp_dir, f"tts_{uuid.uuid4()}.mp3")
        
        try:
            logger.info(f"Generating TTS for text: {text[:50]}... with lang: {gtts_lang}")
            # Chuyển text thành speech
            tts = gTTS(text=text, lang=gtts_lang, slow=False)
            tts.save(filename)
            logger.info(f"TTS file saved to: {filename}")
            
            # Trả về file audio
            response = FileResponse(
                open(filename, 'rb'), 
                content_type='audio/mpeg'
            )
            response['Content-Disposition'] = 'attachment; filename="tts.mp3"'
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            
            # Xóa file sau khi trả về (có thể gây lỗi trên Windows)
            # os.remove(filename)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating TTS: {e}")
            return Response({
                'success': False,
                'error': f'Lỗi tạo giọng nói: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except json.JSONDecodeError:
        return Response({
            'success': False,
            'error': 'Dữ liệu JSON không hợp lệ'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        logger.error(f"Error in tts_gtts: {e}")
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Lỗi hệ thống TTS.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

