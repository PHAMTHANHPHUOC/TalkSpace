<template>
  <div class="luyen-noi-container">
    <!-- Sidebar có thể thu gọn -->
    <div class="sidebar" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <div class="sidebar-header">
        <h3>Chức năng khác</h3>
        <button @click="toggleSidebar" class="toggle-btn">
          <i class="bx" :class="sidebarCollapsed ? 'bx-menu' : 'bx-x'"></i>
        </button>
      </div>
      <div class="sidebar-content" v-if="!sidebarCollapsed">
        <p class="sidebar-description">
          Thanh chọn các chức năng khác, chưa update, có thể click cho nó thu gọn và mở rộng ra
        </p>
        <div class="menu-items">
          <div class="menu-item">
            <i class="bx bx-book-open"></i>
            <span>Bài học</span>
          </div>
          <div class="menu-item">
            <i class="bx bx-trophy"></i>
            <span>Thành tích</span>
          </div>
          <div class="menu-item">
            <i class="bx bx-cog"></i>
            <span>Cài đặt</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Khu vực chat chính -->
    <div class="chat-main">
  

      <!-- Khu vực hiển thị tin nhắn -->
      <div class="chat-messages" ref="messagesContainer">
        <div 
          v-for="(message, index) in messages" 
          :key="index"
          class="message"
          :class="message.type"
        >
          <div class="message-avatar">
            <div class="avatar" :class="message.type">
              <i class="bx" :class="message.type === 'user' ? 'bx-user' : 'bx-bot'"></i>
            </div>
          </div>
          <div class="message-content">
            <div class="message-bubble">
              {{ message.text }}
            </div>
            <div class="message-time">{{ message.time }}</div>
          </div>
        </div>

        <!-- Tin nhắn đang ghi âm -->
        <div v-if="isRecording && currentSpeechText" class="message user">
          <div class="message-avatar">
            <div class="avatar user">
              <i class="bx bx-user"></i>
            </div>
          </div>
          <div class="message-content">
            <div class="message-bubble recording">
              <div class="recording-indicator">
                <span class="pulse"></span>
                <span class="pulse"></span>
                <span class="pulse"></span>
              </div>
              {{ currentSpeechText }}
            </div>
          </div>
        </div>
      </div>

      <!-- Khu vực điều khiển -->
      <div class="chat-controls">
        <div class="control-buttons">
          <button 
            @click="toggleRecording" 
            class="record-btn"
            :class="{ 'recording': isRecording }"
          >
            <i class="bx" :class="isRecording ? 'bx-stop' : 'bx-microphone'"></i>
            {{ isRecording ? 'Dừng' : 'Bắt đầu nói' }}
          </button>
        </div>
        
        <div class="input-area">
          <input 
            v-model="textInput" 
            @keyup.enter="sendTextMessage"
            placeholder="Hoặc nhập tin nhắn..."
            class="text-input"
          />
          <button @click="sendTextMessage" class="send-btn">
            <i class="bx bx-send"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LuyenNoi',
  data() {
    return {
      sidebarCollapsed: false,
      isRecording: false,
      messages: [
        {
          type: 'ai',
          text: 'Xin chào! Tôi là trợ lý AI. Hãy bắt đầu luyện nói tiếng Anh với tôi nhé!',
          time: this.getCurrentTime()
        }
      ],
      currentSpeechText: '',
      textInput: ''
    }
  },
  methods: {
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed;
    },
    toggleRecording() {
      this.isRecording = !this.isRecording;
      if (this.isRecording) {
        this.startRecording();
      } else {
        this.stopRecording();
      }
    },
    startRecording() {
      // Giả lập việc ghi âm
      this.currentSpeechText = 'Đang nghe...';
      // Ở đây sẽ tích hợp với Web Speech API
      console.log('Bắt đầu ghi âm');
    },
    stopRecording() {
      if (this.currentSpeechText && this.currentSpeechText !== 'Đang nghe...') {
        this.messages.push({
          type: 'user',
          text: this.currentSpeechText,
          time: this.getCurrentTime()
        });
        
        // Giả lập phản hồi AI
        setTimeout(() => {
          this.messages.push({
            type: 'ai',
            text: 'Tôi đã hiểu bạn nói: "' + this.currentSpeechText + '". Hãy tiếp tục luyện tập nhé!',
            time: this.getCurrentTime()
          });
          this.scrollToBottom();
        }, 1000);
      }
      
      this.currentSpeechText = '';
      console.log('Dừng ghi âm');
    },
    sendTextMessage() {
      if (this.textInput.trim()) {
        this.messages.push({
          type: 'user',
          text: this.textInput,
          time: this.getCurrentTime()
        });
        
        // Giả lập phản hồi AI
        setTimeout(() => {
          this.messages.push({
            type: 'ai',
            text: 'Bạn đã nhập: "' + this.textInput + '". Tôi sẽ giúp bạn luyện nói!',
            time: this.getCurrentTime()
          });
          this.scrollToBottom();
        }, 1000);
        
        this.textInput = '';
        this.scrollToBottom();
      }
    },
    getCurrentTime() {
      const now = new Date();
      return now.getHours().toString().padStart(2, '0') + ':' + 
             now.getMinutes().toString().padStart(2, '0');
    },
    scrollToBottom() {
      this.$nextTick(() => {
        if (this.$refs.messagesContainer) {
          this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight;
        }
      });
    }
  },
  mounted() {
    this.scrollToBottom();
  }
}
</script>

<style scoped>
.luyen-noi-container {
  display: flex;
  height: 100vh;
  background: #f5f5f5;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Sidebar */
.sidebar {
  width: 280px;
  background: #2c3e50;
  color: white;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.sidebar-collapsed {
  width: 60px;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #34495e;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.toggle-btn {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  padding: 5px;
  border-radius: 5px;
  transition: background 0.2s;
}

.toggle-btn:hover {
  background: #34495e;
}

.sidebar-content {
  padding: 20px;
  flex: 1;
}

.sidebar-description {
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 30px;
  color: #bdc3c7;
}

.menu-items {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.menu-item:hover {
  background: #34495e;
}

.menu-item i {
  font-size: 20px;
}

/* Chat Main */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
}

.chat-header {
  padding: 20px 30px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
}

.chat-header h2 {
  margin: 0;
  color: #2c3e50;
  font-weight: 600;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #7f8c8d;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #27ae60;
  transition: all 0.3s;
}

.status-dot.recording {
  background: #e74c3c;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

/* Messages */
.chat-messages {
  flex: 1;
  padding: 20px 30px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message {
  display: flex;
  gap: 12px;
  max-width: 80%;
}

.message.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message.ai {
  align-self: flex-start;
}

.message-avatar {
  flex-shrink: 0;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: white;
}

.avatar.user {
  background: #3498db;
}

.avatar.ai {
  background: #2ecc71;
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.message-bubble {
  padding: 12px 16px;
  border-radius: 18px;
  max-width: 100%;
  word-wrap: break-word;
  line-height: 1.4;
}

.message.user .message-bubble {
  background: #3498db;
  color: white;
  border-bottom-right-radius: 5px;
}

.message.ai .message-bubble {
  background: #ecf0f1;
  color: #2c3e50;
  border-bottom-left-radius: 5px;
}

.message-bubble.recording {
  background: #f39c12;
  color: white;
  display: flex;
  align-items: center;
  gap: 10px;
}

.recording-indicator {
  display: flex;
  gap: 3px;
}

.pulse {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: white;
  animation: pulse 1s infinite;
}

.pulse:nth-child(2) {
  animation-delay: 0.2s;
}

.pulse:nth-child(3) {
  animation-delay: 0.4s;
}

.message-time {
  font-size: 12px;
  color: #95a5a6;
  align-self: flex-end;
}

.message.user .message-time {
  align-self: flex-start;
}

/* Controls */
.chat-controls {
  padding: 20px 30px;
  border-top: 1px solid #e0e0e0;
  background: white;
}

.control-buttons {
  display: flex;
  justify-content: center;
  margin-bottom: 15px;
}

.record-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  background: #3498db;
  color: white;
}

.record-btn:hover {
  background: #2980b9;
  transform: translateY(-2px);
}

.record-btn.recording {
  background: #e74c3c;
  animation: pulse 2s infinite;
}

.record-btn.recording:hover {
  background: #c0392b;
}

.input-area {
  display: flex;
  gap: 10px;
  align-items: center;
}

.text-input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 25px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.text-input:focus {
  border-color: #3498db;
}

.send-btn {
  width: 45px;
  height: 45px;
  border: none;
  border-radius: 50%;
  background: #3498db;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  transition: all 0.3s;
}

.send-btn:hover {
  background: #2980b9;
  transform: scale(1.1);
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    z-index: 1000;
    transform: translateX(-100%);
  }
  
  .sidebar:not(.sidebar-collapsed) {
    transform: translateX(0);
  }
  
  .chat-main {
    margin-left: 0;
  }
  
  .message {
    max-width: 90%;
  }
}
</style>