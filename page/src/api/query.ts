import axios from 'axios'
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

export function downloadAPI(url: string, filename: string) {
  // 使用 axios 发送 GET 请求下载文件
  axios.get(`api/download`, {
    responseType: 'blob',
    headers: {
      'Content-Type': 'application/json'
    },
    params: {
      file_name: url,
    }
  }).then((response) => {
    const blob = new Blob([response.data], { type: response.headers['content-type'] })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename // 设置下载的文件名
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
  }).catch((error) => {
    console.error('Download error:', error)
  })
}

export function testQueryAPI(data: { query: string }) {
  return new Promise<any>((resolve) => {
    setTimeout(() => {
      resolve(getTestResponse());
    }, 1)
  })
}