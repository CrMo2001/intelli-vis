import request from '../utils/request'
import { getTestResponse } from './testResponse'

export function test(data: { key: string }) {
  return request({
    url: '/test',
    method: 'post',
    data: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

export function queryAPI(data: { query: string }) {
  return request({
    url: '/query',
    method: 'post',
    data: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

export function testQueryAPI(data: { query: string }) {
  return new Promise<any>((resolve) => {
    setTimeout(() => {
      resolve(getTestResponse());
    }, 1)
  })
}