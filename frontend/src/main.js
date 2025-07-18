import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Client from './layout/wrapper/ClientMaster.vue'
import Blank from './layout/wrapper/index_blank.vue'
const app = createApp(App)

app.use(router)
app.component("client-layout", Client);
app.component("blank-layout", Blank);

app.mount("#app")