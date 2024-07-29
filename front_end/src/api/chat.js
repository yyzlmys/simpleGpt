import request from "@/utils/request"


// list chatConversation
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

// get response
export function api_getResponse(data) {
  return request({
    url: `/message/ask`,
    method: 'post',
    data
  })
}

// get conversation
export function api_getConversationName(id) {
  return request({
    url: `/conversation/name/${id}`,
    method: 'get',
  })
}
