import request from "@/utils/request"

// 获取该用户所有知识库
export function api_listKnowledgeBases() {
    return request({
      url: `/lib`,
      method: 'get'
    })
}

// 创建新的知识库
export function api_createKnowledgeBase(data) {
  return request({
    url: `/lib`,
    method: 'post',
    data
  })
}

// 删除某个知识库
export function api_deleteKnowledgeBase(id) {
  return request({
    url: `/lib/${id}`,
    method: 'delete'
  })
}

// 获取某个知识库信息
export function api_getKnowledgeBase(id) {
  return request({
    url: `/lib/get/${id}`,
    method: 'get'
  })
}

// 根据知识库id 获取所有文件信息
export function api_listFiles(libId) {
  return request({
    url: `/file/list/${libId}`,
    method: 'get'
  })
}

// 根据知识库id上传文件
export function api_uploadFile(libId, file) {
  const formData = new FormData();
  formData.append('libId', libId);
  formData.append('file', file)
  return request({
    url: `/file/upload`,
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 根据文件id下载文件
export function api_downloadFile(id) {
  return request({
    url: `/file/load/${id}`,
    method: 'get',
    responseType: 'blob',
  })
}

// 根据文件id删除文件
export function api_deleteFile(id) {
  return request({
    url: `/file/${id}`,
    method: 'delete'
  })
}