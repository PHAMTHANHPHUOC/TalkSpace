import axios from "axios";
const apiUrl = 'http://127.0.0.1:8000/';
import { createToaster } from "@meforma/vue-toaster";
const toaster = createToaster({ position: "top-right" });

function handleError(res) {
    // Nếu có lỗi chi tiết
    if (res.response && res.response.data) {
        const data = res.response.data;
        if (data.errors) {
            Object.values(data.errors).forEach((v) => {
                toaster.error(v[0]);
            });
        } else if (data.message) {
            toaster.error(data.message);
        } else if (data.detail) {
            toaster.error(data.detail);
        } else {
            toaster.error("Đã xảy ra lỗi không xác định!");
        }
    } else {
        toaster.error("Lỗi kết nối máy chủ!");
    }
    // Ném lại lỗi để component có thể xử lý tiếp
    throw res;
}

export default {
    getHeader() {
        let token = window.localStorage.getItem('chia_khoa');
        if (!token) {
            return {};
        }
        return { Authorization: 'Bearer ' + token };
    },
    get(url) {
        return axios.get(apiUrl + url, { headers: this.getHeader() })
            .catch(handleError);
    },
    post(url, data) {
        return axios.post(apiUrl + url, data, { headers: this.getHeader() })
            .catch(handleError);
    },
    delete(url) {
        return axios.delete(apiUrl + url, { headers: this.getHeader() })
            .catch(handleError);
    },
    put(url, data) {
        return axios.put(apiUrl + url, data, { headers: this.getHeader() })
            .catch(handleError);
    },
};