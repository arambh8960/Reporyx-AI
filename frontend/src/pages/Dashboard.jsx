import React, { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import DashboardCard from '../components/DashboardCard'
import { FaGithub, FaComments, FaFileAlt, FaCogs, FaCheckCircle, FaExclamationCircle } from 'react-icons/fa'
import api from '../services/api'
import RepositoryAnalyzer from '../components/RepositoryAnalyzer'

const Dashboard = () => {
  const { currentUser, logout } = useAuth()
  const [backendStatus, setBackendStatus] = useState('loading')
  const [backendMessage, setBackendMessage] = useState('')

  useEffect(() => {
    checkBackendHealth()
  }, [])

  const checkBackendHealth = async () => {
    try {
      const response = await api.get('/health')
      if (response.data.status === 'success') {
        setBackendStatus('connected')
        setBackendMessage(response.data.message)
      } else {
        setBackendStatus('error')
        setBackendMessage('Backend returned unexpected status')
      }
    } catch (error) {
      setBackendStatus('error')
      setBackendMessage('Unable to connect to backend')
    }
  }

  const futureFeatures = [
    {
      title: 'Repository Analysis',
      description: 'Analyze GitHub repositories with AI-powered code understanding',
      icon: FaGithub,
      disabled: true
    },
    {
      title: 'Repository Chat',
      description: 'Chat with your repositories using natural language',
      icon: FaComments,
      disabled: true
    },
    {
      title: 'Repository Summary',
      description: 'Get comprehensive summaries of any codebase',
      icon: FaFileAlt,
      disabled: true
    },
    {
      title: 'Tech Stack Detection',
      description: 'Automatically detect technologies and frameworks',
      icon: FaCogs,
      disabled: true
    }
  ]

  return (
    <div className="min-h-[calc(100vh-100px)] px-4 py-12">
      <div className="max-w-7xl mx-auto">
        {/* Welcome Section */}
        <div className="glass-card p-8 mb-8 animate-fadeIn">
          <h1 className="text-4xl font-bold gradient-text mb-4">
            Welcome, {currentUser?.name || 'User'}!
          </h1>
          <p className="text-white/70 text-lg">
            You're now logged in to CodeGraph AI. Explore the dashboard and get ready to analyze repositories.
          </p>
        </div>

        {/* Status Cards */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {/* Authentication Status */}
          <div className="glass-card p-6 animate-fadeIn" style={{ animationDelay: '0.2s' }}>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-white">Authentication Status</h3>
              <div className="p-3 bg-green-500/20 rounded-xl">
                <FaCheckCircle className="text-2xl text-green-400" />
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex items-center text-white/80">
                <span className="w-24 text-sm">Status:</span>
                <span className="text-green-400 font-medium">Authenticated</span>
              </div>
              <div className="flex items-center text-white/80">
                <span className="w-24 text-sm">Email:</span>
                <span className="text-white">{currentUser?.email}</span>
              </div>
              <div className="flex items-center text-white/80">
                <span className="w-24 text-sm">User ID:</span>
                <span className="text-white/60 text-sm">{currentUser?.id?.substring(0, 8)}...</span>
              </div>
            </div>
          </div>

          {/* Backend Status */}
          <div className="glass-card p-6 animate-fadeIn" style={{ animationDelay: '0.4s' }}>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-white">Backend Status</h3>
              <div className={`p-3 rounded-xl ${backendStatus === 'connected' ? 'bg-green-500/20' : backendStatus === 'loading' ? 'bg-blue-500/20' : 'bg-red-500/20'}`}>
                {backendStatus === 'connected' ? (
                  <FaCheckCircle className="text-2xl text-green-400" />
                ) : backendStatus === 'loading' ? (
                  <div className="w-6 h-6 border-2 border-blue-400 border-t-transparent rounded-full animate-spin" />
                ) : (
                  <FaExclamationCircle className="text-2xl text-red-400" />
                )}
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex items-center text-white/80">
                <span className="w-24 text-sm">Status:</span>
                <span className={`font-medium ${backendStatus === 'connected' ? 'text-green-400' : backendStatus === 'loading' ? 'text-blue-400' : 'text-red-400'}`}>
                  {backendStatus === 'connected' ? 'Connected' : backendStatus === 'loading' ? 'Checking...' : 'Disconnected'}
                </span>
              </div>
              <div className="flex items-center text-white/80">
                <span className="w-24 text-sm">Message:</span>
                <span className="text-white">{backendMessage}</span>
              </div>
            </div>
          </div>
        </div>
        {/* Repository Analyzer */}
<div className="mb-8 animate-fadeIn" style={{ animationDelay: '0.5s' }}>
  <RepositoryAnalyzer />
</div>

        {/* Future Features Section */}
        <div className="animate-fadeIn" style={{ animationDelay: '0.6s' }}>
          <h2 className="text-2xl font-bold text-white mb-6">Coming Soon</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {futureFeatures.map((feature, index) => (
              <DashboardCard
                key={index}
                title={feature.title}
                description={feature.description}
                icon={feature.icon}
                disabled={feature.disabled}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
