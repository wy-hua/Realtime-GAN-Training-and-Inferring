import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import  SocketIO from './plugins/io'
//
// createApp(App).mount('#app')
// app.use(ElementPlus)
const app = createApp(App)
app.use(ElementPlus)
app.use(SocketIO,{
    //ip:port
    connection: 'ws://localhost:5000',
})
app.mount('#app')
