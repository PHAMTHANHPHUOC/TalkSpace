import axios from "axios";
import { createToaster } from "@meforma/vue-toaster";
const toaster = createToaster({ position: "top-right" });

export default function (to, from, next) {
  const token = localStorage.getItem("chia_khoa");
  if (!token) {
    // Nếu không có token, chuyển hướng luôn sang đăng nhập
    next("/dang-nhap");
    toaster.error("Bạn chưa đăng nhập!");
    return;
  }
  axios
    .get("http://127.0.0.1:8000/check_login/", {
      headers: {
        Authorization: "Token " + token,
      },
    })
    .then((res) => {
      if (res.data.status) {
        next();
      } else {
        next("/dang-nhap");
        toaster.error(res.data.message);
      }
    })
    .catch((err) => {
      // Nếu có lỗi (ví dụ token sai), cũng chuyển hướng
      next("/dang-nhap");
      toaster.error("Phiên đăng nhập hết hạn hoặc không hợp lệ!");
    });
}