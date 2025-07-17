<template>
    <div class="row row-cols-1 row-cols-lg-2 row-cols-xl-2">
        <div class="col mx-auto">
            <div class="my-4 text-center">
                <img src="https://dzfullstack.com/assets/images/logo-img.png" width="180" alt="">
            </div>
            <div class="card">
                <div class="card-body">
                    <div class="border p-4 rounded">
                        <div class="text-center">
                            <h3 class="">Đăng Nhập</h3>
                            <p>Bạn chưa có tài khoản? 
                                <router-link to="/khach-hang/dang-ky">
                                    <a href="/khach-hang/dang-ky">Đăng Ký</a> 
                                </router-link>
                            </p>
                        </div>
                        <div class="login-separater text-center mb-4">
                            <hr>
                        </div>
                        <div class="form-body">
                            <form class="row g-3">
                                <div class="col-12">
                                    <label class="form-label">Email</label>
                                    <input type="email" v-model="khach_hang.email" class="form-control"
                                        placeholder="Nhập vào Email">
                                </div>
                                <div class="col-12">
                                    <label class="form-label">Mật Khẩu</label>
                                    <div class="input-group">
                                        <input type="password" v-model="khach_hang.password" class="form-control"
                                            placeholder="Nhập vào Mật Khẩu">
                                    </div>
                                </div>
                                <div class="col-12">
                                    <div class="d-grid">
                                        <button type="button" v-on:click="actionDangNhap()" class="btn btn-primary"><i
                                                class="bx bx-user"></i>Đăng Nhập</button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
import { createToaster } from "@meforma/vue-toaster";
import baseRequest from '../../../src/core/baseRequest';
const toaster = createToaster({ position: "top-right" });
export default {
    data() {
        return {
            khach_hang: {}
        }
    },
    mounted() {

    },
    methods: {
        actionDangNhap() {
            baseRequest
                .post('login/', this.khach_hang)
                .then((res) => {
                    if (res.data.status == 1) {
                        console.log(res.data.chia_khoa);
                        toaster.success(res.data.message);
                        localStorage.setItem('chia_khoa', res.data.chia_khoa);
                        localStorage.setItem('ten_kh', res.data.ten_kh);
                        this.khach_hang = {};
                        this.$router.push('/');
                    } else if (res.data.status == 2) {
                        toaster.warning(res.data.message);
                    } else {
                        toaster.error(res.data.message);
                    }
                })
        },
    },
}
</script>
<style></style>