import { createRouter, createWebHistory } from 'vue-router';
import Error403 from '@/views/Error/Error403.vue';
import Error404 from '@/views/Error/Error404.vue';
import ListKnowledgeBase from '@/views/KnowledgeBase/ListKnowlwdgeBase.vue'
import ManageKnowledgeBase from '@/views/KnowledgeBase/ManageKnowledgeBase.vue'
import Chat from '@/views/Chat/ChatView.vue'
import Personal from '@/views/Personal/Personal.vue'
import WelcomePage from '@/views/Welcome/WelcomePage.vue';
import Guide from '@/views/Guide/Guide.vue';
import ListRobots from '@/views/Robots/ListRobots.vue';
import ManageRobot from '@/views/Robots/ManageRobot.vue';

const routes = [
  {
    path: '/',
    redirect: '/welcome'
  },
  {
    path: '/403',
    name: 'Error403',
    component: Error403
  },
  {
    path: '/404',
    name: 'Error404',
    component: Error404
  },
  {
    path: '/knowledgebase',
    name: 'ListKnowledgeBase',
    component: ListKnowledgeBase
  },
  {
    path: '/manageKnowledgeBase/:id',  // 使用占位符 :id
    name: 'ManageKnowlwdgeBase',
    component: ManageKnowledgeBase,
  },
  {
    path: '/personal',
    name: 'Personal',
    component: Personal
  },
  {
    path: '/chat',
    name: 'Chat',
    component: Chat
  },
  {
    path: '/guide',
    name: 'Guide',
    component: Guide
  },
  {
    path: '/welcome',
    name: 'Welcome',
    component: WelcomePage
  },
  
  {
    path: '/robot',
    name: 'ListRobot',
    component: ListRobots
  },

  {
    path: '/robot/manageRobot/:id',  // 使用占位符 :id
    name: 'ManageRobot',
    component: ManageRobot
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
