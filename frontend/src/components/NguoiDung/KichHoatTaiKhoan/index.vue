<template>
    <h1>Bạn đã kích hoạt thành công</h1>
</template>
<script>
import axios from 'axios';
import { createToaster } from "@meforma/vue-toaster";
const toaster = createToaster({ position: "top-right" });
import baseRequest from '../../../../src/core/baseRequest';
export default {
    props: ['id_can_kich_hoat'],
    mounted() {
        this.kichHoatTaiKhoan();
    },
    methods: {
        kichHoatTaiKhoan() {
            baseRequest
                .get('kich-hoat-tai-khoan/'+ this.$route.params.id_can_kich_hoat)
                .then((res) => {
                    if(res.data.status) {
                        toaster.success(res.data.message);
                        setTimeout(() => {
                            this.$router.push('/dang-nhap');
                        }, 1500);
                    } else {
                        toaster.error(res.data.message);
                    }
                })
        }
    },
}
</script>
<style>
    
</style>