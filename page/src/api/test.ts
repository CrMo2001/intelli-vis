import request from '../utils/request'

export function test(data: {key: string}) {
  return request({
    url: '/test',
    method: 'post',
    data: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  })
}
