<template>
  <div>
    <el-container>
      <el-header class="header" style="height: 7vh;">
        <el-row :gutter="20" style="width: 100%;">
          <el-col :span="5">
            <div class="logo">
              <h2>极简智能</h2>
            </div>
          </el-col>
          <el-col :span="11">
            <div class="nav-links">
              <router-link to="/chat" exact class="nav-item" active-class="active-link">首页</router-link>
              <router-link to="/knowledgebase" class="nav-item" active-class="active-link">知识库</router-link>
              <router-link to="/personal" class="nav-item" active-class="active-link">个人中心</router-link>
            </div>
          </el-col>
          <el-col :span="4" :offset="4">
            <div class="login-area">
              <template v-if="!isLogin">
                <button class="btn btn-primary" @click="loginDialogVisible = true">登录</button>
              </template>
              <template v-else>
                <router-link to="/personal" class="username">{{ username }}</router-link>
              </template>
            </div>
          </el-col>
        </el-row>
      </el-header>
      <el-divider></el-divider>
      <!-- 下方主体 -->
      <el-main class="custom-main"  style="height: 91vh;">
        <router-view @want-login="handleToLogin()" @init="init()" />
      </el-main>
    </el-container>
    <el-dialog v-model="loginDialogVisible" width="350">
      <Login @login="handleLogin()"></Login>
    </el-dialog>
  </div>
</template>

<script>
import { getToken } from '@/utils/auth';
import { api_getInfo } from '@/api/personal';
import Login from '@/components/Login.vue'
export default {
  name: 'App',
  components:{
    Login
    },
  mounted() {
    this.init();
  },

  data() {
    return {
      isLogin: false,
      username: '',
      loginDialogVisible: false
    };
  },

  methods:{
    init()
    {
      this.isLogin = false;
      if(getToken())
      {
        this.isLogin = true;
        this.getInfo();
      }
    },

    getInfo()
    {
      api_getInfo()
      .then((response)=>{
        if(response.data.code == 200)
        {
          this.username = response.data.data.username;
        }
      })
    },

    handleToLogin()
    {
      this.loginDialogVisible = true;
    },

    handleLogin()
    {
      this.loginDialogVisible = false;
      this.init();
      this.$router.push('/chat');
    }
  }
}
</script>

<style scoped>

.header {
  height: 7vh;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #dcdcdc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0 20px;
}

.logo h2 {
  margin: 0;
  color: black;
  font-size: 24px;
}

.nav-links {
  display: flex;
  align-items: center;
}

.nav-item {
  margin-right: 50px; 
  text-decoration: none;
  color: black;
  font-weight: bold;
  font-size: 20px;
  transition: color 0.3s, transform 0.3s;
}

.nav-item:hover {
  color: #66b1ff;
  transform: scale(1.1);
}

.active-link {
  color: #66b1ff;
}

.login-area {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.custom-main {
  padding: 20px;
  background-color: #fff;
}

.el-divider--horizontal {
  margin: 0;
}

.btn {
  border: none;
  display: inline-block;
  padding: 10px 20px;
  margin: 0 10px; /* 调整间距 */
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
  background-color: #ffd700;
  color: #333;
  transition: background-color 0.3s, transform 0.3s;
}

.btn-primary {
  background-color: #409EFF;
  color: white;
}

.btn-primary:hover {
  background-color: #66b1ff;
  transform: scale(1.1);
}

.username {
  margin-right: 20px; 
  color: black;
  text-decoration: none;
}
</style>