import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FormView from '../views/FormView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/f/:slug',
      name: 'formView',
      component: FormView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/auth',
      component: () => import('../views/auth/AuthView.vue'),
      children: [
        {
          path: 'login',
          name: 'login',
          component: () => import('../views/auth/Login.vue'),
        },
        {
          path: 'register',
          name: 'register',
          component: () => import('../views/auth/Register.vue'),
        },
      ],
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/Profile.vue'),
      meta: { requiresLogin: true }
    },
    {
      path: '/forms',
      name: 'formList',
      component: () => import('../views/forms/FormList.vue'),
      meta: { requiresLogin: true }
    },
    {
      path: '/forms/:form_id',
      name: 'formDetail',
      component: () => import('../views/forms/FormDetail.vue'),
      meta: { requiresLogin: true }
    },
    {
      path: '/forms/:form_id/elements',
      name: 'formElements',
      component: () => import('../views/forms/FormElements.vue'),
      meta: { requiresLogin: true }
    }
  ],
})

router.beforeEach((to, from, next) => {
  // console.log('To: ', to)
  // console.log('From: ', from)

  if(to.meta.requiresLogin) {
    const access_token = localStorage.getItem('access_token')
    if(!access_token) {
      next({ name: 'login', query: { 'redirect': to.fullPath } })
    }
  }

  next()
})

export default router
