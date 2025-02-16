import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './index.css'
import App from './App.vue'
import router from './router'
import Notifications from '@kyvg/vue3-notification'

const app = createApp(App)
app.use(Notifications)
app.use(createPinia())
app.use(router)
app.mount('#app')
