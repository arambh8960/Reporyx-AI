import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { FaCode, FaUser, FaSignOutAlt } from 'react-icons/fa'

const Navbar = () => {
  const { currentUser, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <nav className="glass-card mx-4 mt-4 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <Link to="/" className="flex items-center space-x-2 group">
          <FaCode className="text-2xl text-blue-400 group-hover:text-purple-400 transition-colors" />
          <span className="text-2xl font-bold gradient-text">CodeGraph AI</span>
        </Link>

        <div className="flex items-center space-x-4">
          {currentUser ? (
            <>
              <div className="flex items-center space-x-2 text-white/80">
                <FaUser className="text-blue-400" />
                <span className="font-medium">{currentUser.name}</span>
              </div>
              <button
                onClick={handleLogout}
                className="btn-secondary flex items-center space-x-2"
              >
                <FaSignOutAlt />
                <span>Logout</span>
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn-secondary">
                Login
              </Link>
              <Link to="/signup" className="btn-primary">
                Sign Up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar
