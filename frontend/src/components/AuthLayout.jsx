import React from 'react'

const AuthLayout = ({ children, title }) => {
  return (
    <div className="min-h-[calc(100vh-100px)] flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        <div className="glass-card p-8 animate-fadeIn">
          <h2 className="text-3xl font-bold text-center mb-8 gradient-text">
            {title}
          </h2>
          {children}
        </div>
      </div>
    </div>
  )
}

export default AuthLayout
