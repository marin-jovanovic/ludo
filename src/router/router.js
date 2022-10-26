import { createRouter, createWebHistory } from 'vue-router';

import IndexPage from '../views/index/IndexPage';
import LoginPage from '../views/login/LoginPage';
import SignupView from '@/views/signup/SingupView.vue';
import GamePage from '@/views/game/GamePage.vue';


import LogoutPage from '../views/logout/LogoutPage';
import SetttingsView from '../views/settings/SettingsView.vue';
import { store } from "@/store/store"


export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/settings',
      name: 'settings',
      component: SetttingsView
    },
    {
      path: '/game/:id',
      name: 'game',
      component: GamePage
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/logout',
      component: LogoutPage
    },
    {
      path: '/',
      name: "index",
      component: IndexPage
    },
  ]
});


function isPublicPath(toPath) {
  const publicPages = ['/login', '/logout', '/signup'];
  const authNotRequired = publicPages.includes(toPath);
  return authNotRequired;
}


// todo fix using global store, not sure if this is creating new instance

router.beforeEach((to, from, next) => {

  let isPublic = isPublicPath(to.path);

  const loggedIn = sessionStorage.getItem('username');

  store.dispatch("setPath", { path: to.path, isPublic: isPublic });

  if (!isPublic && !loggedIn) {
    // router.push("/login")

    // todo fix
    return next({
      path: '/login',
      query: { returnUrl: to.path }
    });
  }

  next();
})
