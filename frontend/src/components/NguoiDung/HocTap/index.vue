<template>
  <div class="ai-layout">
    <!-- Sidebar trái -->
    <div class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="sidebar-toggle" @click="toggleSidebar">
        <i class="bx" :class="sidebarCollapsed ? 'bx-chevron-right' : 'bx-chevron-left'"></i>
      </div>
      <transition name="fade">
        <div v-if="!sidebarCollapsed" class="sidebar-content">
          <div class="sidebar-title">chưa có chức năng nào,...</div>
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
        <!-- Khung message nổi -->
        <div class="message-box">
          <div class="message-title">giống message</div>
          <div class="messages">
            <div v-for="(message, idx) in messages" :key="idx" class="msg-item" :class="message.type">
              <span>{{ message.text }}</span>
            </div>
          </div>
        </div>
      </div>
      <!-- Thanh chức năng dưới cùng -->
      <div class="bottom-bar">
        <div class="bar-item" >
          <!-- Icon microphone -->
          <i v-if="onmic==1" class="bx bx-microphone"></i>
          <!-- Icon microphone off -->
          <i v-else  class="bx bx-microphone-off"></i>
          <!-- Icon pause -->
          <i v-if="stop==0"  class="bx bx-pause"></i>
          <i v-else class="bx bx-play"></i>

          <!-- Icon volume full -->
          <i v-if="volum==1" class="bx bx-volume-full"></i>
          <i v-else class="bx bx-volume-mute"></i>

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
export default {
  name: 'LuyenNoiUI',
  data() {
    return {
      onmic: 0,
      stop: 1,
      volum:0,
      sidebarCollapsed: false,
      messages: [
        { type: 'ai', text: 'Xin chào! Tôi là trợ lý AI.' },
        { type: 'user', text: 'Chào bạn!' }
      ],
    }
  },
  methods: {
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed;
    }
  }
}
</script>

<style scoped>
.bar-item {
  display: flex;
  flex-direction: row; /* Có thể đổi thành column nếu muốn hiển thị dọc */
  justify-content: space-around;
  align-items: center;
  padding: 10px;
  background-color: #ffffff; /* hoặc #f9f9f9 */
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  gap: 15px; /* khoảng cách giữa các icon */
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
  padding: 0 ;
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

@media (max-width: 900px) {
  .ai-avatar { margin-right: 30px; margin-left: 10px; }
  .message-box { right: 2vw; width: 90vw; min-width: 0; }
}
@media (max-width: 600px) {
  .sidebar { display: none; }
  .main-content { padding: 0; }
  .ai-header { font-size: 14px; }
  .ai-avatar { margin: 0; }
  .message-box { right: 0; left: 0; margin: auto; width: 98vw; }
  .bottom-bar { gap: 6px; padding: 10px 0; }
  .bar-item { width: 36px; height: 36px; font-size: 18px; }
}
</style>