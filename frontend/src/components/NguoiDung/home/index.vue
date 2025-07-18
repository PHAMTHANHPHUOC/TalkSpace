<template>
  <div class="">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="text-primary">Danh sách Bài Học</h2>
      <button class="btn btn-success" @click="showModal = true">
        <i class="fa fa-plus"></i> Thêm Bài Học
      </button>
    </div>

    <div class="row g-4">
      <div v-for="(item, idx) in hocVien" :key="idx" class="col-12 col-md-6 col-lg-3">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h5 class="card-title mb-2">{{ item.ho_ten }}</h5>
            <p class="mb-1"><b>Tuổi:</b> {{ item.ngay_sinh }}</p>
            <p class="mb-1"><b>Giới Tính:</b> {{ item.gioi_tinh }}</p>
            <p class="mb-1"><b>Ngôn ngữ học:</b> {{ item.ngon_ngu_hoc}}</p>
            <p class="mb-1"><b>Cấp Độ:</b> {{ item.trinh_do }}</p>
          </div>
        </div>
      </div>
      <div v-if="hocVien.length === 0" class="text-center text-muted mt-5">Chưa có thông tin người học nào.</div>
    </div>

    <!-- Modal nhập thông tin -->
    <div v-if="showModal" class="modal-backdrop-custom">
      <div class="modal-custom">
        <div class="modal-header-custom">
          <h4 class="mb-0">Thêm thông tin người học</h4>
          <button class="btn-close" @click="showModal = false"></button>
        </div>
        <form @submit.prevent="createHocVien">
          <div class="mb-3">
            <label class="form-label">Họ và tên</label>
            <input v-model="form.ho_ten" type="text" class="form-control" placeholder="Nhập họ và tên" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Ngày Sinh</label>
            <input v-model="form.ngay_sinh" type="date" class="form-control" placeholder="Nhập ngày sinh" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Giới Tính</label>
            <select v-model="form.gioi_tinh" class="form-select" required>
              <option value="Nam">Nam</option>
              <option value="Nữ">Nữ</option>
              <option value="Khác">Khác</option>
            </select>
          </div>
          <div class="mb-3">
            <label class="form-label">Ngôn ngữ học</label>
            <select v-model="form.ngon_ngu" class="form-select" required>
              <option value="" disabled>Chọn ngôn ngữ</option>
              <option v-for="item in ngonngu" :key="item.id" :value="item.id">{{ item.ten_ngon_ngu }}</option>
            </select>
          </div>
          <div class="mb-3">
            <label class="form-label">Cấp Độ</label>
            <select v-model="form.trinh_do" class="form-select" required>
              <option value="" disabled>Chọn Cấp Độ</option>
              <option v-for="item in capdo" :key="item.id" :value="item.id">{{ item.ten_cap_do }}</option>
            </select>
          </div>

          <div class="d-flex justify-content-end gap-2 mt-4">
            <button type="button" class="btn btn-secondary" @click="showModal = false">Hủy</button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm"></span>
              <span v-else>Lưu</span>
            </button>
          </div>
          <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
          <div v-if="success" class="alert alert-success mt-3">{{ success }}</div>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import * as THREE from 'three';
import { createToaster } from "@meforma/vue-toaster";
import baseRequest from '../../../../src/core/baseRequest';
import axios from 'axios';
export default {
  data() {
    return {
      form: {
      ho_ten: '',
      ngay_sinh: '',
      gioi_tinh: 'Nam',
      ngon_ngu: '',
      trinh_do: '',
    },
      hocVien: [],
      capdo: [],
      ngonngu : [],
      showModal: false,
    };
  },
  mounted() {
    this.DataHocVien()
    this.DataCapDo();
    this.DataNgonNgu();
  },
  methods: {
    DataHocVien() {
      const token = localStorage.getItem("chia_khoa");
      axios.get('ho-so-hoc-tap/data',{
        headers: {
                    Authorization: "Token " + token,
                },
        })
            .then((res) => {
                this.hocVien = res.data.data
            })
    },
    DataCapDo() {
        baseRequest
            .get('cap-do/data')
            .then((res) => {
                this.capdo = res.data.data
            })
    },
    DataNgonNgu() {
        baseRequest
            .get('ngon-ngu/data')
            .then((res) => {
                this.ngonngu = res.data.data
            })
    },

    createHocVien() {
        const token = localStorage.getItem("chia_khoa");
        axios
            .post('http://127.0.0.1:8000/ho-so-hoc-tap/create', this.form,{
              headers: {
                        Authorization: "Token " + token,
                    },
            })
            .then((res) => {
                if(res.data.status) {
                    toastr.success(res.data.message);
                    this.DataHocVien();
                    this.form = {}
                }
            })
        },

  },

};
</script>
<style scoped>
.card {
  border-radius: 18px;
  background: #fff;
}
.form-label {
  font-weight: 500;
}
.btn-primary {
  background: linear-gradient(90deg, #4e54c8 0%, #8f94fb 100%);
  border: none;
}
.btn-primary:hover {
  background: linear-gradient(90deg, #8f94fb 0%, #4e54c8 100%);
}
.btn-success {
  background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
  border: none;
}
.btn-success:hover {
  background: linear-gradient(90deg, #38f9d7 0%, #43e97b 100%);
}
.modal-backdrop-custom {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.3);
  z-index: 1050;
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-custom {
  background: #fff;
  border-radius: 16px;
  max-width: 420px;
  width: 100%;
  padding: 2rem 1.5rem 1.5rem 1.5rem;
  box-shadow: 0 8px 32px rgba(60,60,100,0.18);
  animation: fadeIn .2s;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: none; }
}
.modal-header-custom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}
.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  color: #888;
  cursor: pointer;
}
</style>