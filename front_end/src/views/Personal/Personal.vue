<template>
  <div class="container">
    <el-descriptions v-loading="loading" class="info-section" title="个人信息" :column="1" border>
      <el-descriptions-item>
        <template #label>
          <el-icon :style="iconStyle">
            <user />
          </el-icon>
          用户名
        </template>
        {{ info.username }}
      </el-descriptions-item>
      <template #extra>
        <el-button type="primary" size="large" @click="changeUsername">修改用户名</el-button>
        <el-button type="primary" size="large" @click="changePassword">修改密码</el-button>
      </template>
    </el-descriptions>

    <div class="action-buttons">
      <el-button type="danger" size="large" @click="logout">退出登录</el-button>
      <el-button type="danger" size="large" @click="reallyDeactivateAccount">注销账号</el-button>
    </div>

    <div class="theme-switcher">
      <el-button @click="setLightTheme" class="theme-toggle-btn" size="large">浅色模式 ☀️</el-button>
      <el-button @click="setGreenTheme" class="theme-toggle-btn" size="large">护眼模式 👁️</el-button>
    </div>
  </div>
</template>

<script>
import { api_changePassword, api_deactivateAccount, api_getInfo, api_update } from '@/api/personal';
import { removeToken } from "@/utils/auth";
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
  mounted() {
    this.init();
    // 读取本地存储的主题设置
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme === 'green') {
      this.isGreenTheme = true;
      document.body.classList.add('green-theme');
    } else {
      this.isGreenTheme = false;
      document.body.classList.add('light-theme');
    }
  },
  data() {
    return {
      info: null,
      loading: true,
      isGreenTheme: false, // 默认浅色主题
    };
  },
  methods: {
    async init() {
      this.loading = true;
      await this.getInfo();
      this.loading = false;
    },

    async getInfo() {
      await api_getInfo().then((response) => {
        this.info = response.data.data;
      });
    },

    changeUsername() {
      this.$prompt('请输入昵称', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /.{6,}/,
        inputErrorMessage: '昵称不能少于6位'
      }).then(({ value }) => {
        const username = value;
        api_update(username).then((response) => {
          if (response.data.code == 200) {
            this.$message({
              type: 'success',
              message: '修改成功！'
            });
            this.logout();
          } else {
            this.$message({
              type: 'error',
              message: '修改失败！'
            });
          }
        });
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消修改'
        });
      });
    },

    changePassword() {
      this.$prompt('请输入密码', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /.{6,}/,
        inputErrorMessage: '密码不能少于6位'
      }).then(({ value }) => {
        api_changePassword({ password: value }).then((response) => {
          this.$message({
            type: 'success',
            message: '修改成功！'
          });
          this.logout();
        });
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消修改'
        });
      });
    },

    logout() {
      this.$router.push('/chat');
      removeToken();
      this.$emit('init');
    },

    reallyDeactivateAccount() {
      this.$confirm('此操作将注销账号, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'error',
        center: true
      }).then(() => {
        this.deactivateAccount();
        this.$message({
          type: 'success',
          message: '注销成功!'
        });
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消'
        });
      });
    },
    deactivateAccount() {
      api_deactivateAccount().then((response) => {
        this.logout();
      });
    },

    setLightTheme() {
      this.isGreenTheme = false;
      document.body.classList.add('light-theme');
      document.body.classList.remove('green-theme');
      localStorage.setItem('theme', 'light');
    },

    setGreenTheme() {
      this.isGreenTheme = true;
      document.body.classList.add('green-theme');
      document.body.classList.remove('light-theme');
      localStorage.setItem('theme', 'green');
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  font-size: 18px;
}

.info-section {
  width: 100%;
  max-width: 500px;
  margin-bottom: 30px;
  font-size: 18px;
}

.action-buttons {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-bottom: 20px;
}

.theme-switcher {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.el-button {
  margin: 10px 20px;
}

.theme-toggle-btn {
  background-color: #f0f1f2;
  color: #333;
  border: none;
  font-weight: bold;
  transition: background-color 0.3s, transform 0.3s;
}

.theme-toggle-btn:hover {
  background-color: #d4e9d6;
  transform: scale(1.05);
}
</style>
