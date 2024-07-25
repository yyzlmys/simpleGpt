<template>
    <div class="container">
      <el-descriptions class="info-section" title="个人信息" :column="1" border >
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
          <el-button type="primary" size="small" @click="changeUsername">修改用户名</el-button>
          <el-button type="primary" size="small" @click="changePassword">修改密码</el-button>
        </template>
      </el-descriptions>
  
      <div class="action-buttons">
        <el-button type="danger" @click="logout">退出登录</el-button>
        <el-button type="danger" @click="reallyDeactivateAccount">注销账号</el-button>
      </div>
    </div>
</template>

<script>
import { api_changePassword, api_deactivateAccount, api_getInfo, api_update } from '@/api/personal';
import { removeToken } from "@/utils/auth";

export default {
  mounted() {
    this.init();
  },
  data() {
    return {
      info: null
    };
  },
  methods: {
    init() {
      this.getInfo();
    },

    getInfo() {
      api_getInfo().then((response) => {
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
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.info-section {
  width: 100%;
  max-width: 400px;
  margin-bottom: 20px;
}

.action-buttons {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.el-button {
  margin: 10px 10px;
}
</style>