import api from './api'

/**
 * User signup
 * @param {string} name - User's full name
 * @param {string} email - User's email address
 * @param {string} password - User's password
 * @returns {Promise} Response with user data
 */
export const signup = async (name, email, password) => {
  const response = await api.post('/auth/signup', {
    name,
    email,
    password,
  })
  return response.data
}

/**
 * User login
 * @param {string} email - User's email address
 * @param {string} password - User's password
 * @returns {Promise} Response with access token
 */
export const login = async (email, password) => {
  const response = await api.post('/auth/login', {
    email,
    password,
  })
  return response.data
}

/**
 * Store JWT token in localStorage
 * @param {string} token - JWT access token
 */
export const setToken = (token) => {
  localStorage.setItem('token', token)
}

/**
 * Get JWT token from localStorage
 * @returns {string|null} JWT token or null
 */
export const getToken = () => {
  return localStorage.getItem('token')
}

/**
 * Remove JWT token from localStorage
 */
export const removeToken = () => {
  localStorage.removeItem('token')
}

/**
 * Check if user is authenticated
 * @returns {boolean} True if token exists
 */
export const isAuthenticated = () => {
  return !!getToken()
}
