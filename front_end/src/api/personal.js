import request from "@/utils/request"

// 登录函数
export function api_login(data) {
  return request({
    url: `/login`,
    method: 'post',
    data
  })
}

// 注册函数
export function api_signup(data) {
  return request({
    url: `/signup`,
    method: 'post',
    data
  })
}

// 注销账号
export function api_deactivateAccount() {
    return request({
      url: `/user`,
      method: 'delete'
    })
}

// 获取用户信息
export function api_getInfo() {
    return request({
      url: `/getInfo`,
      method: 'get'
    })
}

// 更改用户名
export function api_update(username) {
    return request({
      url: `/changeUsername/${username}`,
      method: 'put',
    })
}

// 修改密码
export function api_changePassword(data) {
  return request({
    url: `/changePassword`,
    method: 'put',
    data
  })
}
    