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
      path: '/visualize',
      name: 'visualize',
      component: () => import('../views/VisualizationView.vue'),
    },
  ],
})

export default router
