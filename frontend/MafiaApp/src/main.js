import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import store from './states/store.js'

createApp(App).use(store).mount('#app');
