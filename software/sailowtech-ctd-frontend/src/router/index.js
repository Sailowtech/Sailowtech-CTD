import { createRouter, createWebHistory } from 'vue-router'
import QuickAccessView from '../views/QuickAccessView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'quickaccess',
      component: QuickAccessView,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
  ],
})

export default router
