import {
    createRouter,
    createWebHistory
} from 'vue-router';

import IndexPage from '../views/index/IndexPage';
import LoginPage from '../views/login/LoginPage';
import SignupView from '@/views/signup/SingupView.vue';
import GamePage from '@/views/game/GamePage.vue';
import GameReplayPage from "@/views/gameReplay/GameReplayPage.vue";
import GameCreatePage from "@/views/gameCreate/GameCreatePage.vue";
import NotFound from '../views/notFound/NotFound';
import waitingRoom from "@/views/waitingRoom/WaitingRoom.vue";
import playingOrder from "@/views/order/PlayingOrder.vue";

import LogoutPage from '../views/logout/LogoutPage';
import SetttingsView from '../views/settings/SettingsView.vue';
import {
    store
} from "@/store/store"

import TheGame from '../views/game/TheGame.vue';

export const router = createRouter({
    history: createWebHistory(),
    routes: [{
            path: '/',
            name: "index",
            component: IndexPage
        },
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
            path: '/gameReplay/:id',
            name: 'gameReplay',
            component: GameReplayPage
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
            path: "/test",
            name: "test",
            component: TheGame
        },
        {
            path: "/gameCreate",
            name: "gameCreate",
            component: GameCreatePage
        }, 
        {
            path: "/waitingRoom/:id",
            name: "waitingRoom",
            component: waitingRoom
        }, 
        {
            path: "/playingOrder/:id",
            name: "playingOrder",
            component: playingOrder
        }, 
        { path: '/:pathMatch(.*)*', component: NotFound },
    ]
});


import {
    userMetaSS
} from '../scripts/session_storage';



function isPublicPath(toPath) {
    const publicPages = ['/login', '/logout', '/signup'];
    const authNotRequired = publicPages.includes(toPath);
    return authNotRequired;
}


router.beforeEach((to, from, next) => {

    let isPublic = isPublicPath(to.path);

    // const loggedIn = ssw.get('username');

    const loggedIn = userMetaSS.isAuth();


    store.dispatch("setPath", {
        path: to.path,
        isPublic: isPublic
    });

    if (!isPublic && !loggedIn) {

        // todo fix when nested url (game/x)  goes to (game/login)
        return next({
            path: '/login',
            query: {
                returnUrl: to.path
            }
        });
    }

    next();
})