// 使用 sessionStorage 管理 token
// 封装成函数

export function getToken() 
{
    return sessionStorage.getItem('token');
}
  
export function setToken(token) 
{
    sessionStorage.setItem('token', token);
}
  
export function removeToken() 
{
    sessionStorage.removeItem('token');
}
