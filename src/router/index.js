import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FormView from '../views/FormView.vue'
import Builder from '../views/forms/Builder.vue'


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
      path: '/thankYou',
      name: 'thankYou',
      component: () => import('../views/ThankYou.vue')
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
      path: '/auth/login',
      name: 'login',
      component: () => import('../views/auth/Login.vue'),
    },
    {
      path: '/auth/register',
      name: 'register',
      component: () => import('../views/auth/Register.vue'),
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
      path: '/forms/:form_id/submissions',
      name: 'formSubmissions',
      component: () => import('../views/forms/submissions/SubmissionList.vue'),
      meta: { requiresLogin: true }
    },
    {
      path: '/forms/:formId/builder',
      name: 'builder',
      component: Builder,
      meta: { requiresLogin: true },
      props: true
    },
    {
      path: '/forms/:form_id/builder-old',
      name: 'formBuilder',
      component: () => import('../views/forms/builder/FormBuilder.vue'),
      meta: { requiresLogin: true }
    },
    { path: '/:pathMatch(.*)*', 
      component: () => import('../views/404.vue') 
    },
  ],
})

router.beforeEach((to, from, next) => {
  if(to.meta.requiresLogin) {
    const access_token = localStorage.getItem('access_token')
    if(!access_token) {
      next({ name: 'login', query: { 'redirect': to.fullPath } })
    } else {
      next()
    }
  } else {
    next()
  }

})

export default router
