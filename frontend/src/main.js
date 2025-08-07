import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Client from './layout/wrapper/ClientMaster.vue'
import Blank from './layout/wrapper/index_blank.vue'
import i18n from './i18n' 
const app = createApp(App)

app.use(router)
app.use(i18n)
app.component("client-layout", Client);
app.component("blank-layout", Blank);

app.mount("#app")