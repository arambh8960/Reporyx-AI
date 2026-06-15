import React, { createContext, useContext, useState, useEffect } from 'react'
import { login as loginService, signup as signupService, setToken, removeToken, getToken } from '../services/authService'

const AuthContext = createContext(null)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is logged in on mount
    const token = getToken()
    if (token) {
      // Decode token to get user info (basic implementation)
      // In production, you might want to validate the token with the backend
      try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        setCurrentUser({
          id: payload.sub,
          email: payload.email,
          name: payload.email.split('@')[0] // Fallback name from email
        })
      } catch (error) {
        console.error('Error decoding token:', error)
        removeToken()
      }
    }
    setLoading(false)
  }, [])

  const login = async (email, password) => {
    try {
      const response = await loginService(email, password)
      setToken(response.access_token)
      
      // Decode token to get user info
      const payload = JSON.parse(atob(response.access_token.split('.')[1]))
      setCurrentUser({
        id: payload.sub,
        email: payload.email,
        name: payload.email.split('@')[0]
      })
      
      return response
    } catch (error) {
      throw error
    }
  }

  const signup = async (name, email, password) => {
    try {
      const response = await signupService(name, email, password)
      return response
    } catch (error) {
      throw error
    }
  }

  const logout = () => {
    removeToken()
    setCurrentUser(null)
  }

  const value = {
    currentUser,
    loading,
    login,
    signup,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
