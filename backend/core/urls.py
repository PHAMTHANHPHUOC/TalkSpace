from django.urls import path,re_path
from .views import view_KhachHang,view_HoSoHocTap,view_VoiceChatAPI,view_GPTAPI



app_name = 'core'

urlpatterns = [
    path('', view_KhachHang.home, name='home'),
    path('login/',view_KhachHang.login),
    path('signup/',view_KhachHang.signup),
    path('check_login/',view_KhachHang.check_login),
    path('quen-mat-khau/',view_KhachHang.quen_mat_khau),
    path('lay-lai-mat-khau/<str:hash_reset>/', view_KhachHang.actionLaylaiMK),
    path('logout/',view_KhachHang.logout),
    path('logout-all/',view_KhachHang.logout_all),
    path('kich-hoat-tai-khoan/<str:hash_active>/', view_KhachHang.kich_hoat_tai_khoan, name='kich_hoat_tai_khoan'),

    path('ho-so-hoc-tap/create',view_HoSoHocTap.create_HoSo),
    path('ho-so-hoc-tap/delete/<int:id>/',view_HoSoHocTap.delete_HoSo),
    path('ho-so-hoc-tap/data',view_HoSoHocTap.data_HoSo),
    #lấy id của table hồ sơ được học
    path('ho-so-hoc-tap/language',view_HoSoHocTap.get_user_language),
    path('cap-do/data',view_HoSoHocTap.data_CapDo),
    path('ngon-ngu/data',view_HoSoHocTap.data_NgonNgu),
    path('chu-de/data',view_HoSoHocTap.data_ChuDe),
    
    # Voice Chat API endpoints
    #chuyển giọng nói thành văn bản
    path('voice-chat/record-transcribe/', view_VoiceChatAPI.record_and_transcribe, name='record_and_transcribe'),
    #chuyển đổi âm thanh được truyền vào thành văn bản text
    path('voice-chat/transcribe-file/', view_VoiceChatAPI.transcribe_audio_file, name='transcribe_audio_file'),
    #chuyển âm thanh từ dạng base64 sang text
    path('voice-chat/transcribe-base64/', view_VoiceChatAPI.transcribe_base64_audio, name='transcribe_base64_audio'),
    
    # GPT API endpoints
    #chát với chatGPT bằng text
    path('gpt/chat/', view_GPTAPI.chat_with_gpt, name='chat_with_gpt'),
    #chat voi chatgpt bằng voice
    # path('gpt/voice-chat/', view_GPTAPI.voice_chat_with_gpt, name='voice_chat_with_gpt'),
    #Dùng để test key
    path('gpt/status/', view_GPTAPI.check_api_status, name='check_api_status'),
    
    # TTS API endpoints
    #Chuyển văn bản thành giọng nói
    path('tts/gtts/', view_GPTAPI.tts_gtts, name='tts_gtts'),
    



]




