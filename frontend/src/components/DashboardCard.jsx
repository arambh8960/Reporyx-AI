import React from 'react'
import { FaLock } from 'react-icons/fa'

const DashboardCard = ({ title, description, icon: Icon, disabled = false }) => {
  return (
    <div
      className={`glass-card p-6 transition-all duration-300 hover:scale-105 ${
        disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:shadow-2xl'
      }`}
    >
      <div className="flex items-start justify-between mb-4">
        <div
          className={`p-3 rounded-xl ${
            disabled ? 'bg-white/5' : 'bg-gradient-to-br from-blue-500/20 to-purple-500/20'
          }`}
        >
          {disabled ? (
            <FaLock className="text-2xl text-white/40" />
          ) : (
            <Icon className="text-2xl text-blue-400" />
          )}
        </div>
        {disabled && (
          <span className="px-3 py-1 bg-white/10 rounded-full text-xs text-white/60">
            Coming Soon
          </span>
        )}
      </div>
      <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
      <p className="text-white/70 text-sm">{description}</p>
    </div>
  )
}

export default DashboardCard
