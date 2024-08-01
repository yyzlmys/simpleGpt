import request from "@/utils/request"

// list robot
export function api_listRobots() {
  return request({
    url: `/robot/list`,
    method: 'get'
  })
}
