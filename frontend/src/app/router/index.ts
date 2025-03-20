import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'logics',
      component: () => import('@/pages/logics/LogicsPage.vue'),
    },
  ],
});

export default router;
