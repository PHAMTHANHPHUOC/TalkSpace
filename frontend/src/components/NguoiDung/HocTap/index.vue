<template>
  <div class="ai-layout">
    <!-- Sidebar trái -->
    <div class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="sidebar-toggle" @click="toggleSidebar">
        <i class="bx" :class="sidebarCollapsed ? 'bx-chevron-right' : 'bx-chevron-left'"></i>
      </div>
      <transition name="fade">
        <div v-if="!sidebarCollapsed" class="sidebar-content">
          <div class="sidebar-title">Voice Chat Settings</div>
          <div class="settings-section">
            <div class="setting-item">
              <label>Recording Duration (s):</label>
              <input 
                type="number" 
                v-model="recordingDuration" 
                min="1" 
                max="30"
                :disabled="isRecording"
                class="setting-input"
              >
            </div>
            <div class="setting-item">
              <label>Recognition Method:</label>
              <div class="radio-group">
                <label class="radio-label">
                  <input 
                    type="radio" 
                    v-model="useWhisper" 
                    :value="true"
                    :disabled="isRecording"
                  >
                  Whisper (More Accurate)
                </label>
                <label class="radio-label">
                  <input 
                    type="radio" 
                    v-model="useWhisper" 
                    :value="false"
                    :disabled="isRecording"
                  >
                  Google STT (Faster)
                </label>
              </div>
            </div>
             <div class="mb-3 setting-item ">
            <label class="form-label">Chọn Chủ Đề</label>
            <select v-model="form.chu_de" class="form-select" required>
              <option value="" disabled>Chọn Chủ Đề</option>
              <option v-for="item in chude" :key="item.id" :value="item.id">{{ item.ten_chu_de }}</option>
            </select>
          </div>
           <div class="mb-3 setting-item ">
            <label class="form-label">Cấp Độ</label>
            <select v-model="form.trinh_do" class="form-select" required>
              <option value="" disabled>Chọn Cấp Độ</option>
              <option v-for="item in capdo" :key="item.id" :value="item.id">{{ item.ten_cap_do }}</option>
            </select>
          </div>
       
            <div class="setting-item">
              <button @click="getLearningSuggestions" class="suggestions-button">
                <i class="bx bx-lightbulb"></i>
                Lấy gợi ý học tập
              </button>
            </div>
            

          </div>
        </div>
      </transition>
    </div>

    <!-- Main content -->
    <div class="main-content">
      <!-- Dòng chữ trên đầu -->
      <!-- <div class="ai-header"><img style="height: 50px;width: 50px;" src="/src/assets/images/iconnew.png" alt=""></div> -->
      <div class="ai-center-area">
        <!-- Avatar AI -->
        <div class="ai-avatar">
          <img src="../../../assets/images/AI.jpg" alt="">
        </div>
        
        <!-- Start Session Button -->
        <div v-if="!sessionStarted" class="start-session-container">
          <div class="start-session-card">
            <div class="start-icon">
              <i class="bx bx-play-circle"></i>
            </div>
            <h3 class="start-title">Bắt đầu phiên học tập</h3>
            <p class="start-description">
              Nhấn Start để bắt đầu trò chuyện với AI và luyện tập kỹ năng nói
            </p>
            <button @click="startSession" class="start-button">
              <i class="bx bx-play me-2"></i>
              Start Learning Session
            </button>
          </div>
        </div>

        <!-- Khung message nổi -->
        <div v-if="sessionStarted" class="message-box">
          <div class="message-title">Conversation</div>
          <div class="messages">
            <div v-for="(message, idx) in messages" :key="idx" class="msg-item" :class="message.type">
              <span>{{ message.text }}</span>
            </div>
            <!-- Recording indicator -->
            <div v-if="isRecording" class="msg-item recording-indicator">
              <div class="recording-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <span>Recording... {{ recordingTime }}s</span>
            </div>
            <!-- Processing indicator -->
            <div v-if="isProcessing" class="msg-item processing-indicator">
              <div class="spinner"></div>
              <span>Processing audio...</span>
            </div>
          </div>
          
          <!-- Text Input Section -->
          <div class="text-input-section">
            <div class="input-group">
              <input 
                v-model="textInput"
                @keyup.enter="sendTextMessage"
                type="text" 
                placeholder="Nhập tin nhắn hoặc nhấn Enter..."
                class="text-input"
                :disabled="isProcessing"
              >
              <button 
                @click="sendTextMessage"
                :disabled="!textInput.trim() || isProcessing"
                class="send-button"
              >
                <i class="bx bx-send"></i>
              </button>
            </div>
            <div class="input-tabs">
              <button 
                @click="inputMode = 'text'"
                :class="['tab-button', { active: inputMode === 'text' }]"
              >
                <i class="bx bx-edit"></i>
                Text
              </button>
              <button 
                @click="inputMode = 'voice'"
                :class="['tab-button', { active: inputMode === 'voice' }]"
              >
                <i class="bx bx-microphone"></i>
                Voice
              </button>
            </div>
          </div>
        </div>
      </div>
      <!-- Thanh chức năng dưới cùng -->
      <div class="bottom-bar">
        <div class="bar-item" >
          <!-- Icon microphone - chỉ hiển thị khi session đã start -->
          <i  
            v-if="sessionStarted"
            @click="toggleOnmic" 
            v-show="inputMode === 'voice' && onmic==0" 
            class="bx bx-microphone"
            :class="{ 'recording': isRecording }"
          ></i>
          <!-- Icon microphone off -->
          <i  
            v-if="sessionStarted"
            @click="toggleOnmic" 
            v-show="inputMode === 'voice' && onmic==1"  
            class="bx bx-microphone-off"
            :class="{ 'recording': isRecording }"
          ></i>
          
          <!-- Icon text input -->
          <i  
            v-if="sessionStarted"
            @click="inputMode = 'text'"
            v-show="inputMode === 'voice'"
            class="bx bx-edit"
            :class="{ 'active': inputMode === 'text' }"
          ></i>
          
          <!-- Icon pause -->
          <i @click="toggleStop" v-if="stop==0"  class="bx bx-pause"></i>
          <i @click="toggleStop" v-else class="bx bx-play"></i>

          <!-- Icon volume full -->
          <i @click="togglevolum" v-if="volum==1" class="bx bx-volume-full"></i>
          <i @click="togglevolum" v-else class="bx bx-volume-mute"></i>

          <!-- Icon send -->
          <!-- <i class="bx bx-send"></i> -->

          <!-- Icon settings/cog -->
          <i class="bx bx-cog"></i>

          <!-- Icon user -->
          <i class="bx bx-user"></i>

          <!-- Icon book open -->
          <i class="bx bx-book-open"></i>

          <!-- Icon trophy -->
          <i class="bx bx-trophy"></i>

          <!-- Icon message -->
          <i class="bx bx-message"></i>

          <!-- Icon dots horizontal rounded -->
          <i class="bx bx-dots-horizontal-rounded"></i>

        </div>
        <div class="bar-item more">...</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import baseRequest from '../../../../src/core/baseRequest';

export default {
  name: 'LuyenNoiUI',
  data() {
    return {
      form: {
      chu_de: '',
      trinh_do: '',
    },
      onmic: 0,
      stop: 0,
      volum: 0,
      capdo: [],
      chude : [],
      hosoList: [], // Danh sách hồ sơ học tập
      selectedHosoId: null, // ID hồ sơ được chọn
      sidebarCollapsed: false,
      sessionStarted: false,
      isRecording: false,
      isProcessing: false,
      isProcessingTTS: false,
      userLanguage: 'vi', // Ngôn ngữ mặc định
  // Tự động phát TTS
      recordingDuration: 5,
      useWhisper: true,
      recordingTime: 0,
      recordingTimer: null,
      mediaRecorder: null,
      audioChunks: [],
      messages: [
        { type: 'ai', text: 'Xin chào! Tôi là trợ lý AI. Nhấn Start để bắt đầu phiên học tập.' },
        { type: 'ai', text: 'Tôi sẽ giúp bạn luyện tập kỹ năng nói và trả lời các câu hỏi.' }
      ],
      textInput: '',
      inputMode: 'text', // 'text' or 'voice'
      selectedTopic: '',
      selectedLevel: '',
    }
  },
  mounted() {
    // this.DataHocVien()
    this.DataCapDo();
    this.DataNgonNgu();
    this.DataHoSo(); // Lấy danh sách hồ sơ học tập
  },
  methods: {
    DataCapDo() {
        axios
            .get('http://127.0.0.1:8000/cap-do/data')
            .then((res) => {
                console.log('Cap do data response:', res.data);
                this.capdo = res.data.data || []
            })
            .catch((error) => {
                console.error('Error fetching cap do data:', error);
                this.capdo = []
            })
    },
    DataNgonNgu() {
        axios
            .get('http://127.0.0.1:8000/chu-de/data')
            .then((res) => {
                console.log('Chu de data response:', res.data);
                this.chude = res.data.data || []
            })
            .catch((error) => {
                console.error('Error fetching Chu de data:', error);
                this.chude = []
            })
    },
    DataHoSo() {
        const token = localStorage.getItem("chia_khoa");
        if (!token) {
            console.log('No token found, cannot fetch hoso data');
            return;
        }
        
        axios
            .get('http://127.0.0.1:8000/ho-so-hoc-tap/data', {
                headers: {
                    Authorization: "Token " + token,
                },
            })
            .then((res) => {
                console.log('Ho so data response:', res.data);
                this.hosoList = res.data.data || [];
                // Tự động chọn hồ sơ đầu tiên nếu có
                if (this.hosoList.length > 0) {
                    this.selectedHosoId = this.hosoList[0].id;
                    this.getUserLanguage(); // Lấy ngôn ngữ sau khi có hồ sơ
                }
            })
            .catch((error) => {
                console.error('Error fetching ho so data:', error);
                this.hosoList = [];
            })
    },
    getUserLanguage() {
        const token = localStorage.getItem("chia_khoa");
        if (!token) {
            console.log('No token found, using default language');
            return;
        }
        
        if (!this.selectedHosoId) {
            console.log('No hoso selected, using default language');
            this.userLanguage = 'vi';
            return;
        }
        
        console.log('Fetching user language for hoso ID:', this.selectedHosoId);
        axios
            .get(`http://127.0.0.1:8000/ho-so-hoc-tap/language?hoso_id=${this.selectedHosoId}`, {
                headers: {
                    Authorization: "Token " + token,
                },
            })
            .then((res) => {
                console.log('User language response:', res.data);
                if (res.data.success && res.data.language) {
                    // Sử dụng mã gTTS từ database
                    this.userLanguage = res.data.language.gtts_code || 'vi';
                    console.log('Set user language to:', this.userLanguage);
                    console.log('Language details:', {
                        id: res.data.language.id,
                        name: res.data.language.name,
                        code: res.data.language.code,
                        gtts_code: res.data.language.gtts_code
                    });
                } else {
                    console.log('No language found in response, using default vi');
                    this.userLanguage = 'vi';
                }
            })
            .catch((error) => {
                console.error('Error fetching user language:', error);
                // Sử dụng ngôn ngữ mặc định nếu có lỗi
                this.userLanguage = 'vi';
                console.log('Using default language due to error:', this.userLanguage);
            })
    },
    onHosoChange() {
        console.log('Hồ sơ học tập đã thay đổi:', this.selectedHosoId);
        if (this.selectedHosoId) {
            this.getUserLanguage(); // Lấy ngôn ngữ mới cho hồ sơ đã chọn
        }
    },
    startSession() {
      this.sessionStarted = true;
      this.messages = [
        { type: 'ai', text: '🎉 Phiên học tập đã bắt đầu!' },
        { type: 'ai', text: 'Bạn có thể nhập text hoặc sử dụng microphone để nói chuyện với tôi.' },
        { type: 'ai', text: 'Tôi sẽ lắng nghe và trả lời các câu hỏi của bạn.' }
      ];
      // Thêm hiệu ứng chuyển động
      setTimeout(() => {
        this.messages.push({ 
          type: 'ai', 
          text: '💡 Mẹo: Bạn có thể chuyển đổi giữa Text và Voice bằng các tab bên dưới.' 
        });
      }, 2000);
    },

    async toggleOnmic() {
      if (this.inputMode !== 'voice') {
        this.inputMode = 'voice';
        return;
      }
      this.onmic = this.onmic === 1 ? 0 : 1

      if (this.onmic === 1) {
        await this.startRecording()
      } else {
        this.stopRecording()
      }
    },

    async startRecording() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        this.mediaRecorder = new MediaRecorder(stream)
        this.audioChunks = []
        this.isRecording = true
        this.startRecordingTimer()

        this.mediaRecorder.ondataavailable = (e) => {
          this.audioChunks.push(e.data)
        }

        this.mediaRecorder.onstop = async () => {
          await this.processRecording()
        }

        this.mediaRecorder.start()
        // Auto-stop after duration
        setTimeout(() => {
          if (this.isRecording) {
            this.stopRecording()
          }
        }, this.recordingDuration * 1000)

      } catch (error) {
        console.error('Error accessing microphone:', error)
        this.messages.push({ 
          type: 'ai', 
          text: '❌ Không thể truy cập microphone. Vui lòng sử dụng chế độ Text để nhập tin nhắn.' 
        })
        this.inputMode = 'text';
        // this.onmic = 0
      }
    },

    stopRecording() {
      if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
        this.mediaRecorder.stop()
        this.mediaRecorder.stream.getTracks().forEach(track => track.stop())
      }
      this.isRecording = false
      this.stopRecordingTimer()
    },

    startRecordingTimer() {
      this.recordingTime = 0
      this.recordingTimer = setInterval(() => {
        this.recordingTime++
      }, 1000)
    },

    stopRecordingTimer() {
      if (this.recordingTimer) {
        clearInterval(this.recordingTimer)
        this.recordingTimer = null
      }
    },

    // async processRecording() {
    //   this.isProcessing = true
      
    //   try {
    //     const blob = new Blob(this.audioChunks, { type: 'audio/wav' })
    //     const base64Audio = await this.blobToBase64(blob)

    //     // Sử dụng GPT API cho voice chat
    //     const response = await baseRequest.post('/gpt/voice-chat/', {
    //       audio_base64: base64Audio,
    //       topic: this.selectedTopic,
    //       level: this.selectedLevel,
    //       use_whisper: this.useWhisper
    //     })

    //     if (response.data.success) {
    //       const userText = response.data.transcription.text
    //       this.messages.push({ type: 'user', text: userText })
          
    //       // Hiển thị phản hồi từ GPT
    //       if (response.data.gpt_response.success) {
    //         this.messages.push({ 
    //           type: 'ai', 
    //           text: response.data.gpt_response.response
    //         })
    //       } else {
    //         this.messages.push({ 
    //           type: 'ai', 
    //           text: `⚠️ Lỗi GPT: ${response.data.gpt_response.error}` 
    //         })
    //       }
    //     } else {
    //       this.messages.push({ 
    //         type: 'ai', 
    //         text: `⚠️ Lỗi nhận diện: ${response.data.error}. Vui lòng thử lại hoặc sử dụng chế độ Text.` 
    //       })
    //     }

    //   } catch (error) {
    //     console.error('Error processing recording:', error)
    //     this.messages.push({ 
    //       type: 'ai', 
    //       text: '❌ Có lỗi xảy ra khi xử lý audio. Vui lòng thử lại hoặc sử dụng chế độ Text.' 
    //     })
    //   } finally {
    //     this.isProcessing = false
    //     this.onmic = 0
    //   }
    // },

    blobToBase64(blob) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = () => {
          const base64 = reader.result.split(',')[1]
          resolve(base64)
        }
        reader.onerror = reject
        reader.readAsDataURL(blob)
      })
    },

    async sendTextMessage() {
      if (this.textInput.trim()) {
        const userMessage = this.textInput.trim();
        this.messages.push({ type: 'user', text: userMessage });
        
        // Clear input
        this.textInput = '';
        
        // Gửi tin nhắn lên GPT API
        this.isProcessing = true;
        
        try {
          const response = await baseRequest.post('gpt/chat/', {
            message: userMessage,
            topic: this.selectedTopic,
            level: this.selectedLevel
          });

          if (response.data.success) {
            const aiMessage = { 
              type: 'ai', 
              text: response.data.response
            };
            this.messages.push(aiMessage);
            
            // Tự động phát TTS cho tin nhắn AI
            this.playTTS(aiMessage.text);
          } else {
            this.messages.push({ 
              type: 'ai', 
              text: `⚠️ Lỗi GPT: ${response.data.error}` 
            });
          }
        } catch (error) {
          console.error('Error sending message to GPT:', error);
          this.messages.push({ 
            type: 'ai', 
            text: '❌ Có lỗi xảy ra khi kết nối với GPT. Vui lòng thử lại.' 
          });
        } finally {
          this.isProcessing = false;
        }
      }
    },

    async playTTS(text) {
      if (!text || this.isProcessingTTS) return;
      
      console.log('TTS Request - Text:', text, 'Language:', this.userLanguage);
      console.log('TTS Request Body:', { text, lang: this.userLanguage });
      this.isProcessingTTS = true;
      try {
        const response = await fetch('http://127.0.0.1:8000/tts/gtts/', {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + localStorage.getItem("chia_khoa")
          },
          body: JSON.stringify({ 
            text,
            lang: this.userLanguage // Gửi ngôn ngữ từ database
          })
        });
        
        if (response.ok) {
          const blob = await response.blob();
          const url = URL.createObjectURL(blob);
          const audio = new Audio(url);
          
          audio.onended = () => {
            URL.revokeObjectURL(url); // Giải phóng bộ nhớ
          };
          
          await audio.play();
        } else {
          const errorData = await response.json();
          console.error('TTS Error:', errorData);
          alert('Không thể chuyển văn bản thành giọng nói!');
        }
      } catch (error) {
        console.error('TTS Error:', error);
        alert('Lỗi khi phát âm thanh!');
      } finally {
        this.isProcessingTTS = false;
      }
    },

    toggleStop() {
      this.stop = this.stop === 1 ? 0 : 1
    },
    
    togglevolum() {
      this.volum = this.volum === 1 ? 0 : 1
    },
    
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed;
    },


    async getLearningSuggestions() {
      // Kiểm tra xem đã chọn chủ đề và cấp độ chưa
      if (!this.form.chu_de || !this.form.trinh_do) {
        this.messages.push({ 
          type: 'ai', 
          text: '⚠️ Vui lòng chọn cả chủ đề và cấp độ trước khi lấy gợi ý học tập.' 
        });
        return;
      }

      this.isProcessing = true;
      
      // Lấy tên chủ đề và cấp độ từ dữ liệu
      const selectedChuDe = this.chude.find(item => item.id === this.form.chu_de);
      const selectedCapDo = this.capdo.find(item => item.id === this.form.trinh_do);
      
      const chuDeName = selectedChuDe ? selectedChuDe.ten_chu_de : '';
      const capDoName = selectedCapDo ? selectedCapDo.ten_cap_do : '';
      
      this.messages.push({ 
        type: 'user', 
        text: `Tôi muốn học về "${chuDeName}" ở cấp độ "${capDoName}".` 
      });

      try {
        const response = await baseRequest.post('gpt/chat/', {
          message: `Hãy đưa ra gợi ý học tập cho chủ đề "${chuDeName}" ở cấp độ "${capDoName}".`,
          topic_id: this.form.chu_de,
          level_id: this.form.trinh_do
        });

        if (response.data.success) {
          const aiMessage = { 
            type: 'ai', 
            text: `💡 Gợi ý học tập cho "${chuDeName}" (${capDoName}):\n\n${response.data.response}` 
          };
          this.messages.push(aiMessage);
          
          // Tự động phát TTS cho tin nhắn AI
          this.playTTS(aiMessage.text);
        } else {
          this.messages.push({ 
            type: 'ai', 
            text: `⚠️ Không thể lấy gợi ý cho chủ đề "${chuDeName}" với trình độ "${capDoName}". Vui lòng thử lại.` 
          });
        }
      } catch (error) {
        console.error('Error getting learning suggestions:', error);
        this.messages.push({ 
          type: 'ai', 
          text: '❌ Có lỗi xảy ra khi lấy gợi ý học tập. Vui lòng thử lại.' 
        });
      } finally {
        this.isProcessing = false;
      }
    }
  },

  beforeUnmount() {
    this.stopRecording()
    this.stopRecordingTimer()
  }
}
</script>

<style scoped>
.bar-item {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  padding: 10px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  gap: 15px;
}

.bar-item i {
  font-size: 24px;
  color: #555;
  padding: 10px;
  border-radius: 50%;
  transition: all 0.3s ease;
  cursor: pointer;
}

.bar-item i:hover {
  background-color: #e0e0e0;
  color: #000;
  transform: scale(0.9);
}

.bar-item i.recording {
  color: #dc3545;
  animation: pulse 1.5s infinite;
}

.bar-item i.active {
  color: #3498db;
  background-color: #e3f2fd;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.7;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.ai-layout {
  display: flex;
  height: 768px;
  width: 1700px;
  background: #f7fafd;
  overflow: hidden;
}

.sidebar {
  width: 180px;
  height: 766px;
  min-width: 60px;
  background: #222c36;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  transition: width 0.3s cubic-bezier(.4,2,.6,1);
  position: relative;
  box-shadow: 2px 0 8px #0001;
  z-index: 2;
}

.sidebar.collapsed {
  width: 60px;
}

.sidebar-toggle {
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0;
  cursor: pointer;
  font-size: 24px;
  background: #1a222b;
  border-bottom: 1px solid #2d3742;
}

.sidebar-content {
  padding: 24px 16px;
  font-size: 16px;
  line-height: 1.6;
  color: #cfd8dc;
}

.sidebar-title {
  font-weight: 500;
  font-size: 15px;
  margin-bottom: 20px;
}

.settings-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.setting-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.setting-item label {
  font-size: 14px;
  color: #cfd8dc;
}

.setting-input {
  background: #1a222b;
  border: 1px solid #2d3742;
  color: #cfd8dc;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 14px;
}

.setting-input:focus {
  outline: none;
  border-color: #3498db;
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  cursor: pointer;
}

.radio-label input[type="radio"] {
  margin: 0;
}

.suggestions-button {
  background: linear-gradient(135deg, #f39c12, #e67e22);
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  justify-content: center;
}

.suggestions-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(243, 156, 18, 0.3);
}

.suggestions-button:active {
  transform: translateY(0);
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: stretch;
  position: relative;
  overflow: hidden;
  height: 80vh;
}

.ai-header {
  text-align: center;
  font-size: 16px;
  color: #222;
  margin-top: 18px;
  margin-bottom: 0;
  font-weight: 400;
  letter-spacing: 0.2px;
}

.ai-center-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  min-height: 0;
}

.ai-avatar {
  z-index: 1;
  margin-right: 120px;
  margin-left: 40px;
}

/* Start Session Styles */
.start-session-container {
  position: absolute;
  right: 16px;
  bottom: 24px;
  top: auto;
  transform: none;
  width: 340px;
  z-index: 2;
}

.start-session-card {
  background: #fff;
  border-radius: 22px;
  box-shadow: 0 4px 32px #0002;
  padding: 32px 24px;
  text-align: center;
  border: 1.5px solid #e3e8ee;
  animation: slideInUp 0.5s ease-out;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.start-icon {
  font-size: 64px;
  color: #3498db;
  margin-bottom: 16px;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

.start-title {
  font-size: 24px;
  font-weight: 600;
  color: #2d3742;
  margin-bottom: 12px;
}

.start-description {
  font-size: 14px;
  color: #718096;
  margin-bottom: 24px;
  line-height: 1.5;
}

.start-button {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 50px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.start-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4);
}

.start-button:active {
  transform: translateY(0);
}

.message-box {
  position: absolute;
  right: 16px;
  bottom: 24px;
  top: auto;
  transform: none;
  width: 340px;
  min-height: 120px;
  background: #fff;
  border-radius: 22px;
  box-shadow: 0 4px 32px #0002;
  padding: 24px 20px 18px 20px;
  display: flex;
  flex-direction: column;
  z-index: 2;
  border: 1.5px solid #e3e8ee;
  animation: slideInUp 0.5s ease-out;
}

.message-title {
  font-size: 17px;
  font-weight: 500;
  color: #2d3742;
  margin-bottom: 10px;
}

.messages {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 200px;
  overflow-y: auto;
}

.msg-item {
  font-size: 15px;
  padding: 8px 14px;
  border-radius: 12px;
  background: #f2f6fa;
  color: #222;
  align-self: flex-start;
  max-width: 90%;
}

.msg-item.user {
  background: #3498db;
  color: #fff;
  align-self: flex-end;
}

.recording-indicator {
  background: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
  display: flex;
  align-items: center;
  gap: 8px;
}

.recording-dots {
  display: flex;
  gap: 4px;
}

.recording-dots span {
  width: 6px;
  height: 6px;
  background: #856404;
  border-radius: 50%;
  animation: recordingDots 1.4s infinite;
}

.recording-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.recording-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes recordingDots {
  0%, 60%, 100% {
    transform: scale(1);
    opacity: 0.4;
  }
  30% {
    transform: scale(1.2);
    opacity: 1;
  }
}

.processing-indicator {
  background: #d1ecf1;
  color: #0c5460;
  border: 1px solid #bee5eb;
  display: flex;
  align-items: center;
  gap: 8px;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #0c5460;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.bottom-bar {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  padding: 0;
  background: #f7fafd;
  border-top: 1.5px solid #e3e8ee;
}

.bar-item {
  width: 44px;
  height: 44px;
  background: #fff;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  color: #222c36;
  box-shadow: 0 2px 8px #0001;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
}

.bar-item:hover {
  background: #e3e8ee;
  box-shadow: 0 4px 16px #0002;
}

.bar-item.more {
  font-size: 26px;
  color: #b0b8c1;
  background: transparent;
  box-shadow: none;
  cursor: default;
}

.text-input-section {
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #e3e8ee;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-group {
  display: flex;
  gap: 10px;
  align-items: center;
  background: #f2f6fa;
  border: 1px solid #e3e8ee;
  border-radius: 10px;
  padding: 8px 12px;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05);
}

.text-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 15px;
  color: #222;
  padding: 0;
}

.text-input::placeholder {
  color: #999;
}

.send-button {
  background: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.send-button:hover {
  background: #2980b9;
}

.send-button:disabled {
  background: #ccc;
  cursor: not-allowed;
  color: #666;
}

.input-tabs {
  display: flex;
  gap: 10px;
  margin-top: 10px;
  border-bottom: 1px solid #e3e8ee;
  padding-bottom: 5px;
}

.tab-button {
  background: #f2f6fa;
  border: 1px solid #e3e8ee;
  border-radius: 8px;
  padding: 5px 10px;
  font-size: 14px;
  color: #555;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 5px;
}

.tab-button:hover {
  background: #e3e8ee;
  border-color: #d1d1d1;
  color: #333;
}

.tab-button.active {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

@media (max-width: 900px) {
  .ai-avatar { margin-right: 30px; margin-left: 10px; }
  .message-box, .start-session-container { right: 2vw; width: 90vw; min-width: 0; }
}

@media (max-width: 600px) {
  .sidebar { display: none; }
  .main-content { padding: 0; }
  .ai-header { font-size: 14px; }
  .ai-avatar { margin: 0; }
  .message-box, .start-session-container { right: 0; left: 0; margin: auto; width: 98vw; }
  .bottom-bar { gap: 6px; padding: 10px 0; }
  .bar-item { width: 36px; height: 36px; font-size: 18px; }
}

.tts-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  margin-left: 8px;
  color: #3498db;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.tts-btn:hover {
  color: #e67e22;
  background-color: rgba(230, 103, 34, 0.1);
}

.tts-btn:disabled {
  color: #bdc3c7;
  cursor: not-allowed;
}

.spinner-small {
  width: 14px;
  height: 14px;
  border: 2px solid #3498db;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  display: inline-block;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.toggle-switch {
  display: flex;
  align-items: center;
  margin-top: 5px;
}

.toggle-input {
  display: none;
}

.toggle-label {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 20px;
  background-color: #ccc;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.toggle-label:before {
  content: '';
  position: absolute;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  top: 2px;
  left: 2px;
  background-color: white;
  transition: transform 0.3s;
}

.toggle-input:checked + .toggle-label {
  background-color: #3498db;
}

.toggle-input:checked + .toggle-label:before {
  transform: translateX(20px);
}
</style>