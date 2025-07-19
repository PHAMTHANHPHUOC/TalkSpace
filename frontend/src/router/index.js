import { createRouter, createWebHistory } from "vue-router"; // cài vue-router: npm install vue-router@next --save
import KiemTraKhachHang from './KiemTraKhachHang'
const routes = [
    {
        path: '/', component: () => import('../components/NguoiDung/home/index.vue'),
        meta : {layout : 'client'},
        beforeEnter: KiemTraKhachHang,
    },
    {
        path: '/dang-ky', component: () => import('../components/NguoiDung/DangKy/index.vue'),
        
    },
    {
        path: '/dang-nhap', component: () => import('../components/NguoiDung/DangNhap/index.vue'),
        
    },
        {
        path: '/learning', component: () => import('../components/NguoiDung/HocTap/index.vue'),
        meta : {layout : 'client'},
        beforeEnter: KiemTraKhachHang,
    },
    {
        path: '/kich-hoat-tai-khoan/:id_can_kich_hoat', component: () => import('../components/NguoiDung/KichHoatTaiKhoan/index.vue'),
        
    },
]
const router = createRouter({
    history: createWebHistory(),
    routes: routes
})

export default router