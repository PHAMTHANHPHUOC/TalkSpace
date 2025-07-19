<template>
  <div class="auth-bg">
    <div class="auth-card">
      <canvas ref="effectCanvas" class="effect-canvas"></canvas>
      <div class="logo-box">
        <img src="/src/assets/images/iconnew.png" width="80" alt="AI Logo" />
      </div>
      <h2 class="auth-title">Đăng Ký Tài Khoản AI</h2>
      <form class="auth-form">
        <div class="form-group">
          <label>Họ Và Tên</label>
          <input type="text" v-model="khach_hang_create.ho_va_ten" placeholder="Nhập vào họ và tên" />
        </div>
        <div class="form-group">
          <label>Email</label>
          <input type="email" v-model="khach_hang_create.email" placeholder="Nhập vào Email" />
        </div>
        <div class="form-group">
          <label>Số Điện Thoại</label>
          <input type="text" v-model="khach_hang_create.so_dien_thoai" placeholder="Nhập vào Số điện thoại" />
        </div>
        <div class="form-group">
          <label>Mật Khẩu</label>
          <input type="password" v-model="khach_hang_create.password" placeholder="Nhập vào Mật Khẩu" />
        </div>
        <div class="form-group">
          <label>Nhập Lại Mật Khẩu</label>
          <input type="password" v-model="khach_hang_create.re_password" placeholder="Nhập lại Mật Khẩu" />
        </div>
        <button type="button" class="btn-auth" @click="actionDangKy()">Đăng Ký</button>
        <div class="auth-link">
          Đã có tài khoản? <router-link to="/dang-nhap">Đăng Nhập</router-link>
        </div>
      </form>
    </div>
  </div>
</template>
<script>
import * as THREE from 'three';
import { createToaster } from "@meforma/vue-toaster";
import baseRequest from '../../../../src/core/baseRequest';
const toaster = createToaster({ position: "top-right" });
export default {
  data() {
    return {
      khach_hang_create: {}
    }
  },
  mounted() {
    // Hiệu ứng three.js: sóng ánh sáng trên card
    const canvas = this.$refs.effectCanvas;
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true });
    renderer.setSize(340, 38);
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, 340 / 38, 0.1, 1000);
    camera.position.z = 8;
    const points = [];
    for (let i = -16; i <= 16; i++) {
      points.push(new THREE.Vector3(i, Math.cos(i * 0.4) * 1.1, 0));
    }
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const material = new THREE.LineBasicMaterial({ color: 0x00fff7, linewidth: 2, transparent: true, opacity: 0.5 });
    const line = new THREE.Line(geometry, material);
    scene.add(line);
    function animate() {
      requestAnimationFrame(animate);
      const pos = geometry.attributes.position;
      for (let i = 0; i < pos.count; i++) {
        pos.setY(i, Math.cos(i * 0.4 + Date.now() * 0.002) * 1.1);
      }
      pos.needsUpdate = true;
      renderer.render(scene, camera);
    }
    animate();
  },
  methods: {
    actionDangKy() {
      baseRequest
        .post('signup/', this.khach_hang_create)
        .then((res) => {
          if(res.data.status) {
            toaster.success(res.data.message);
            this.khach_hang_create = {};
          } else {
            toaster.error(res.data.message);
          }
        }); 
    },
  },
}
</script>
<style scoped>
.auth-bg {
  min-height: 100vh;
  background: linear-gradient(120deg, #181c24 60%, #1e2a38 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}
.auth-card {
  background: rgba(24, 28, 36, 0.92);
  border-radius: 22px;
  box-shadow: 0 0 32px #00fff720;
  padding: 38px 32px 28px 32px;
  width: 340px;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.effect-canvas {
  position: absolute;
  left: 0;
  top: 0;
  width: 340px;
  height: 38px;
  pointer-events: none;
  z-index: 0;
}
.logo-box {
  margin-bottom: 10px;
  z-index: 1;
}
.auth-title {
  color: #00fff7;
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 18px;
  letter-spacing: 1px;
  text-shadow: 0 0 8px #00fff720;
  z-index: 1;
}
.auth-form {
  width: 100%;
  z-index: 1;
}
.form-group {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
}
.form-group label {
  color: #b0eaff;
  font-size: 15px;
  margin-bottom: 6px;
}
.form-group input {
  background: rgba(16, 19, 26, 0.92);
  border: 1.5px solid #00fff720;
  border-radius: 10px;
  padding: 10px 14px;
  color: #b0eaff;
  font-size: 15px;
  outline: none;
  box-shadow: 0 0 8px #00fff710;
  transition: border 0.2s;
}
.form-group input:focus {
  border: 1.5px solid #00fff7;
}
.btn-auth {
  width: 100%;
  background: linear-gradient(90deg, #00fff7 60%, #00bfae 100%);
  color: #181c24;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  padding: 12px 0;
  font-size: 16px;
  margin-top: 8px;
  margin-bottom: 10px;
  box-shadow: 0 0 12px #00fff720;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.btn-auth:hover {
  background: linear-gradient(90deg, #00bfae 60%, #00fff7 100%);
  color: #181c24;
}
.auth-link {
  text-align: center;
  color: #b0eaff;
  font-size: 14px;
  margin-top: 8px;
}
.auth-link a {
  color: #00fff7;
  text-decoration: underline;
  margin-left: 4px;
}
</style>