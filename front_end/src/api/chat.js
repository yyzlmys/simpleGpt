import request from "@/utils/request"

// list conversation
export function api_listConversations() {
  return request({
    url: `/conversation/list`,
    method: 'get'
  })
}

// create Conversation
export function api_createConversation(data) {
  return request({
    url: `/conversation`,
    method: 'post',
    data
  })
}

// delete Conversation
export function api_deleteConversation(id) {
  return request({
    url: `/conversation/${id}`,
    method: `delete`,
  })
}

// list chatHistory
export function api_listChatHistory(conversationId) {
  return request({
    url: `/message/list/${conversationId}`,
    method: 'get'
  })
}

// get conversation name
export function api_getConversationName(id) {
  return request({
    url: `/conversation/name/${id}`,
    method: 'get',
  })
}

// get response
export function api_getResponse(data) {
  return request({
    url: `/message/ask`,
    method: 'post',
    data
  })
}

// 上传文件
export function api_getFileResponse(file, question, conversationId) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('question', question)
  formData.append('conversationId', conversationId)
  return request({
    url: `/message/file`,
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 视频机器人回答
export function api_getVideoResponse(data) {
  return request({
    url: `/message/vedio`,
    method: 'post',
    data
  })
}

// 网页机器人回答
export function api_getWebPageResponse(data) {
  return request({
    url: `/message/web`,
    method: 'post',
    data
  })
}
