import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const new_user = (data) => api.post('/users/', data)
export const get_users = () => api.get('/users/')
export const update_user = (id, data) => api.patch(`/users/${id}`, data)

export default api
