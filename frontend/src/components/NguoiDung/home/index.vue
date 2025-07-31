<template>
  <div class="">

    <Toaster />
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 >Danh sách Hồ Sơ Học Tập</h2>
      <div class="d-flex gap-2">
        <!-- <router-link to="/learning" class="btn btn-primary">
          <i class="fa fa-graduation-cap"></i> Bắt đầu Học
        </router-link> -->
        <button class="btn btn-success" @click="showModal = true">
          <i class="fa fa-plus"></i> Thêm Hồ Sơ
        </button>
      </div>
    </div>

    <div v-if="loadingData" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3 text-muted">Đang tải danh sách Bài Học...</p>
    </div>
    
    <div v-else class="row g-4">
      
        <div v-for="(item, idx) in list_HocVien" :key="idx" class="col-12 col-md-6 col-lg-3">
        <div class="card shadow-sm h-500 card-hover">
          <div class="card-body">
            <h5 class="card-title mb-2">{{ item.ho_ten }}</h5>
            <p class="mb-1"><b>Ngày sinh:</b> {{ formatDate(item.ngay_sinh) }}</p>
            <p class="mb-1"><b>Giới tính:</b> {{ item.gioi_tinh }}</p>
            <p class="mb-1"><b>Ngôn ngữ học:</b> {{ getNgonNguName(item.ngon_ngu_hoc_id) }}</p>
           
            
            <div class="mt-3">
              <router-link to="/learning" class="btn btn-primary btn-sm w-100">
                <i class="fa fa-graduation-cap"></i> Bắt đầu Học
              </router-link>
            </div>
            
            <!-- Nút xóa hiện khi hover -->
            <div class="delete-button-container">
              <button 
                class="btn btn-danger btn-sm w-100" 
                @click="confirmDelete(item)"
                title="Xóa hồ sơ"
              >
                <i class="fa fa-trash"></i> Xóa hồ sơ
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="!list_HocVien || list_HocVien.length === 0" class="text-center text-muted mt-5">
        <i class="fa fa-users fa-3x mb-3 text-muted"></i>
        <p>Chưa có hồ sơ học tập nào.</p>
      </div>
    </div>
    <!-- Modal nhập thông tin -->
    <div v-if="showModal" class="modal-backdrop-custom">
      <div class="modal-custom">
        <div class="modal-header-custom">
          <h4 class="mb-0">Thêm thông tin Bài Học</h4>
          <button class="btn-close" @click="closeModal"></button>
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
          <!-- <div class="mb-3">
            <label class="form-label">Cấp Độ</label>
            <select v-model="form.trinh_do" class="form-select" required>
              <option value="" disabled>Chọn Cấp Độ</option>
              <option v-for="item in capdo" :key="item.id" :value="item.id">{{ item.ten_cap_do }}</option>
            </select>
          </div> -->

          <div class="d-flex justify-content-end gap-2 mt-4">
            <button type="button" class="btn btn-secondary" @click="closeModal">Hủy</button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm"></span>
              <span v-else>Lưu</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal xác nhận xóa -->
    <div v-if="showDeleteModal" class="modal-backdrop-custom">
      <div class="modal-custom">
        <div class="modal-header-custom">
          <h4 class="mb-0 text-danger">Xác nhận xóa</h4>
          <button class="btn-close" @click="showDeleteModal = false"></button>
        </div>
        <div class="modal-body">
          <p>Bạn có chắc chắn muốn xóa hồ sơ của <strong>{{ itemToDelete?.ho_ten }}</strong>?</p>
          <p class="text-muted small">Hành động này không thể hoàn tác.</p>
        </div>
        <div class="d-flex justify-content-end gap-2 mt-4">
          <button type="button" class="btn btn-secondary" @click="showDeleteModal = false">Hủy</button>
          <button 
            type="button" 
            class="btn btn-danger" 
            @click="deleteHocVien"
            :disabled="loadingDelete"
          >
            <span v-if="loadingDelete" class="spinner-border spinner-border-sm"></span>
            <span v-else>Xóa</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import * as THREE from 'three';
import { createToaster, Toaster } from "@meforma/vue-toaster";
import axios from 'axios';

const toaster = createToaster({
  position: 'top-right',
  duration: 3000,
});

export default {
  components: {
    Toaster
  },
  data() {
    return {
      form: {
      ho_ten: '',
      ngay_sinh: '',
      gioi_tinh: 'Nam',
      ngon_ngu: '',
      trinh_do: '',
    },
      list_HocVien: [],
      capdo: [],
      ngonngu : [],
      showModal: false,
      showDeleteModal: false,
      loading: false,
      loadingDelete: false,
      loadingData: true,
      itemToDelete: null,
    };
  },
  mounted() {
    this.DataHocVien()
    this.DataCapDo();
    this.DataNgonNgu();
  },
  methods: {
    DataHocVien() {
      this.loadingData = true;
      const token = localStorage.getItem("chia_khoa");
      axios.get('http://127.0.0.1:8000/ho-so-hoc-tap/data',{
        headers: {
                    Authorization: "Token " + token,
                },
        })
            .then((res) => {
                console.log('Hoc vien data response:', res.data);
                console.log('Hoc vien list:', res.data.data);
                this.list_HocVien = res.data.data || []
            })
            .catch((error) => {
                console.error('Error fetching hoc vien data:', error);
                this.list_HocVien = []
            })
            .finally(() => {
                this.loadingData = false;
            })
    },
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
            .get('http://127.0.0.1:8000/ngon-ngu/data')
            .then((res) => {
                console.log('Ngon ngu data response:', res.data);
                this.ngonngu = res.data.data || []
            })
            .catch((error) => {
                console.error('Error fetching ngon ngu data:', error);
                this.ngonngu = []
            })
    },
    createHocVien() {
        // Kiểm tra validation trước
        if (!this.form.ho_ten || !this.form.ngay_sinh || !this.form.ngon_ngu) {
            toaster.error('Vui lòng điền đầy đủ thông tin!');
            return;
        }

        this.loading = true;
        const token = localStorage.getItem("chia_khoa");
        axios
            .post('http://127.0.0.1:8000/ho-so-hoc-tap/create', this.form,{
              headers: {
                        Authorization: "Token " + token,
                    },
            })
            .then((res) => {
                if(res.data.success) {
                    toaster.success(res.data.message || 'Tạo thông tin người học thành công!');
                    this.DataHocVien();
                    this.resetForm();
                    this.showModal = false;
                } else {
                    // Hiển thị lỗi từ server
                    toaster.error(res.data.message || 'Có lỗi xảy ra khi tạo thông tin người học');
                }
            })
            .catch((error) => {
                console.error('Error creating hoc vien:', error);
                if (error.response && error.response.data && error.response.data.message) {
                    toaster.error(error.response.data.message);
                } else {
                    toaster.error('Có lỗi xảy ra khi tạo thông tin người học');
                }
            })
            .finally(() => {
                this.loading = false;
            });
    },

    resetForm() {
        this.form = {
            ho_ten: '',
            ngay_sinh: '',
            gioi_tinh: 'Nam',
            ngon_ngu: '',
            trinh_do: '',
        };
    },

    closeModal() {
        this.showModal = false;
        this.resetForm();
    },

    formatDate(dateString) {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleDateString('vi-VN');
    },

    getNgonNguName(ngonNguId) {
        console.log('Looking for ngon ngu ID:', ngonNguId, 'Available:', this.ngonngu);
        const ngonNgu = this.ngonngu.find(item => item.id === ngonNguId);
        console.log('Found ngon ngu:', ngonNgu);
        return ngonNgu ? ngonNgu.ten_ngon_ngu : 'N/A';
    },

    // getCapDoName(capDoId) {
    //     console.log('Looking for cap do ID:', capDoId, 'Available:', this.capdo);
    //     const capDo = this.capdo.find(item => item.id === capDoId);
    //     console.log('Found cap do:', capDo);
    //     return capDo ? capDo.ten_cap_do : 'N/A';
    // },

    confirmDelete(item) {
        this.itemToDelete = item;
        this.showDeleteModal = true;
    },

    deleteHocVien() {
        if (!this.itemToDelete) return;
        
        this.loadingDelete = true;
        const token = localStorage.getItem("chia_khoa");
        
        axios.delete(`http://127.0.0.1:8000/ho-so-hoc-tap/delete/${this.itemToDelete.id}/`, {
            headers: {
                Authorization: "Token " + token,
            },
        })
        .then((res) => {
            if (res.data.success) {
                toaster.success(res.data.message || 'Xóa hồ sơ thành công!');
                this.DataHocVien(); // Reload danh sách
                this.showDeleteModal = false;
                this.itemToDelete = null;
            } else {
                toaster.error(res.data.message || 'Có lỗi xảy ra khi xóa hồ sơ');
            }
        })
        .catch((error) => {
            console.error('Error deleting hoc vien:', error);
            if (error.response && error.response.data && error.response.data.message) {
                toaster.error(error.response.data.message);
            } else {
                toaster.error('Có lỗi xảy ra khi xóa hồ sơ');
            }
        })
        .finally(() => {
            this.loadingDelete = false;
        });
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

.btn-close:hover {
  color: #333;
}

/* Đảm bảo modal hiển thị trên cùng */
.modal-backdrop-custom {
  z-index: 9999;
}

.modal-custom {
  z-index: 10000;
}

/* Thêm hiệu ứng cho modal */
.modal-custom {
  max-height: 90vh;
  overflow-y: auto;
}

/* Cải thiện form controls */
.form-control:focus,
.form-select:focus {
  border-color: #4e54c8;
  box-shadow: 0 0 0 0.2rem rgba(78, 84, 200, 0.25);
}

/* Nút xóa */
.btn-outline-danger {
  border-color: #dc3545;
  color: #dc3545;
  transition: all 0.3s ease;
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  border-color: #dc3545;
  color: white;
}

.btn-danger {
  background: linear-gradient(90deg, #dc3545 0%, #c82333 100%);
  border: none;
}

.btn-danger:hover {
  background: linear-gradient(90deg, #c82333 0%, #dc3545 100%);
}

/* Modal body */
.modal-body {
  padding: 1rem 0;
}

/* Card hover effect cho nút xóa */
.card-hover {
  position: relative;
  transition: all 0.3s ease;
}

.card-hover:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
}

.delete-button-container {
  margin-top: 0.5rem;
  max-height: 0;
  overflow: hidden;
  opacity: 0;
  transform: translateY(-10px);
  transition: all 0.3s ease;
}

.card-hover:hover .delete-button-container {
  max-height: 50px;
  opacity: 1;
  transform: translateY(0);
  margin-top: 1.5rem;
}

.delete-button-container .btn {
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
  transition: all 0.2s ease;
}

.delete-button-container .btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(220, 53, 69, 0.4);
}
</style>