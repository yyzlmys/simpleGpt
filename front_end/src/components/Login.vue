<template>
    <div class="login-box">
      <el-tabs v-model="activateName"  @tab-click="handleClick">
        <el-tab-pane label="登录" name="login">
          <el-form ref="loginForm" :model="form" :rules="loginRules" class="login-form">
            <el-form-item prop="username">
              <el-input
                placeholder="请输入账号"
                prefix-icon="el-icon-user"
                v-model="form.username">
              </el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input 
              placeholder="请输入密码"
              prefix-icon="el-icon-lock"
              v-model="form.password" 
              show-password></el-input>
            </el-form-item>
            <div style="display: flex; justify-content: flex-start;">
              <el-link type="primary" @click="ResetPassword()">忘记密码?</el-link>
              <br>
            </div>
            <el-form-item style="text-align: center;">
              <el-button type="primary"  @click="login">登录</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="注册" name="signup">
          <el-form ref="loginForm" :model="form" :rules="loginRules" class="login-form">
            <el-form-item prop="username">
              <el-input
                placeholder="请输入账号"
                prefix-icon="el-icon-user"
                v-model="form.username">
              </el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input 
              placeholder="请输入密码"
              prefix-icon="el-icon-lock"
              v-model="form.password" 
              show-password></el-input>
            </el-form-item>
            <el-form-item style="text-align: center;">
              <el-button type="primary"  @click="signup">注册</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </div>
</template>

<script>
import { api_login, api_signup } from '@/api/personal';
import { setToken } from '@/utils/auth';
export default 
{
    name: 'Login',
    data() {
    return {
      activateName:'login',
      form: {
        id: 0,
        username: '',
        password: ''
      },
      loginRules: {
        username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      }
    };
  },
  methods: {
    login() {
      // 实现登录逻辑
      if(this.form.username.length < 6)
      {
        this.$message({
          message: '账号不能少于6位!',
          type: 'warning'
        });
      }
      else if(this.form.password.length < 6)
      {
        this.$message({
          message: '密码不能少于6位!',
          type: 'warning'
        });
      }
      else
      {
        api_login(this.form)
          .then((response)=>
          {
            if(response.data.code == 200)
            {
              this.$message({
                message: '登录成功！',
                type: 'success'
              });
              setToken(response.data.data)
              this.$emit('login');

              this.form.username = '';
              this.form.password = '';
            }
            else
            {
              this.$message({
                message: '用户名或密码错误！',
                type: 'error'
              });
            } 
          })
      }
      
    },
    signup() {
      // 实现注册逻辑
      console.log("注册！！！");
      if(this.form.username.length < 6)
      {
        this.$message({
          message: '账号不能少于6位！',
          type: 'warning'
        });
      }
      else if(this.form.password.length < 6)
      {
        this.$message({
          message: '密码不能少于6位！',
          type: 'warning'
        });
      }
      else
      {
        api_signup(this.form)
          .then((response)=>
          {
            if(response.data.code == 200)
            {
              this.$message({
                message: '注册成功！',
                type: 'success'
              });
              this.form.username = '';
              this.form.password = '';           
            }
            else
            {
              this.$message({
                message: '账号已存在，请选择其他账号！',
                type: 'warning'
              });
              this.form.username = '';
              this.form.password = '';
            } 
          })
      }
    },

    handleClick()
    {
      this.form.username = '';
      this.form.password = '';
    },

    ResetPassword()
    {
      this.$message({
        message: '请您再仔细想一想！！！',
        type: 'success'
      });
    }

  }
};
</script>

<style>

</style>