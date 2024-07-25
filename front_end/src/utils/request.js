// 封装 axios 网络请求，在后续获取所有数据时，必须验证token

import router from '@/router';

import axios from 'axios'
import { getToken } from '@/utils/auth'

// create an axios instance
const service = axios.create({

  // baseURL 根据环境变量改变，使得Mock只拦截Mock环境变量
  baseURL: process.env.VUE_APP_BASE_API, 
  timeout: 5000 
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // do something before request is sent

    // 在所有网络请求的请求头中加 token
    config.headers['X-Token'] = getToken()

    return config
  },
  error => {

    console.log(error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
    (response) => {
        if(response.data.code == 401) //状态码40001: 未授权，需要登录
        {   
          if(router.currentRoute.name != '401')
            router.push('/403');
        }

      return response;
    },
    (error) => {
      // 处理响应错误
      return Promise.reject(error);
    }
);


export default service
