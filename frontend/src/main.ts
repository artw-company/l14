import { createApp } from 'vue';
import router from '@/app/router';
import App from './App.vue';
import '@/assets/scss/index.scss';

const app = createApp(App);

app.use(router);

app.mount('#app');
