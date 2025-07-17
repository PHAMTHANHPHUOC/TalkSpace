import axios from "axios";
import { createToaster } from "@meforma/vue-toaster";
const toaster = createToaster({ position: "top-right" });
export default function (to, from, next) {
  axios
    .get("http://127.0.0.1:8000/check_login/", {
      headers: {
        Authorization: "Token " + localStorage.getItem("chia_khoa"),
      }
      
    })
    .then((res) => {
      console.log("Token:", localStorage.getItem("chia_khoa"));
      if (res.data.status) {
        next();
      } else {
        next("/khach-hang/dang-nhap");
        toaster.error(res.data.message);
        
      }
    });
}
