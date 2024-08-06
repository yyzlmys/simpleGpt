import request from "@/utils/request"

// list robot
export function api_listRobots() {
  return request({
    url: `/robot/list`,
    method: 'get'
  })
}

export function api_create_robot(data) {
  return request({
    url: `/robot`,
    method: 'post',
    data
  })
}

export function api_delete_robot(id) {
    return request({
      url: `/robot/${id}`,
      method: 'delete'
    })
}

// get robot details
export function api_getRobot(id) {
  return request({
    url: `/robot/${id}`,
    method: 'get'
  })
}
