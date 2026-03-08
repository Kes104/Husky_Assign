import { createRouter, createWebHistory } from 'vue-router'

import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import Employee from '../pages/empdash.vue'
import Employer from '../pages/higher-emp.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/employee', component: Employee },
  { path: '/employer', component: Employer },
  { path: '/lapply', component: Employee },
  { path: '/lall', component: Employer },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
