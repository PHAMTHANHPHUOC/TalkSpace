import { createRouter, createWebHistory } from "vue-router"; // cài vue-router: npm install vue-router@next --save
import KiemTraKhachHang from './KiemTraKhachHang'
const routes = [
    {
        path: '/', component: () => import('../components/home/index.vue'),
        meta : {layout : 'client'},
        beforeEnter: KiemTraKhachHang,
    },
    {
        path: '/khach-hang/dang-ky', component: () => import('../components/DangKy/index.vue'),
        meta : {layout : 'client'},
    },
    {
        path: '/khach-hang/dang-nhap', component: () => import('../components/DangNhap/index.vue'),
        meta : {layout : 'client'},
    },
    {
        path: '/khach-hang/kich-hoat-tai-khoan/:id_can_kich_hoat', component: () => import('../components/KichHoatTaiKhoan/index.vue'),
        meta : {layout : 'client'},
    },
]
const router = createRouter({
    history: createWebHistory(),
    routes: routes
})

export default router