import React from 'react'
import { Link } from 'react-router-dom'
import { FaGithub, FaRocket, FaBrain, FaChartLine } from 'react-icons/fa'

const Home = () => {
  return (
    <div className="min-h-[calc(100vh-100px)] flex items-center justify-center px-4 py-12">
      <div className="max-w-6xl mx-auto">
        {/* Hero Section */}
        <div className="text-center mb-16 animate-fadeIn">
          <h1 className="text-5xl md:text-7xl font-bold mb-6">
            <span className="gradient-text">CodeGraph AI</span>
          </h1>
          <p className="text-xl md:text-2xl text-white/80 mb-8 max-w-3xl mx-auto">
            AI-Powered Developer Onboarding Assistant for GitHub Repositories
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/signup" className="btn-primary text-lg">
              <FaRocket className="inline mr-2" />
              Get Started
            </Link>
            <Link to="/login" className="btn-secondary text-lg">
              Login
            </Link>
          </div>
        </div>

        {/* Features Section */}
        <div className="grid md:grid-cols-3 gap-6 mb-16">
          <div className="glass-card p-6 text-center animate-fadeIn" style={{ animationDelay: '0.2s' }}>
            <div className="p-4 bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-xl w-fit mx-auto mb-4">
              <FaBrain className="text-3xl text-blue-400" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">AI-Powered Analysis</h3>
            <p className="text-white/70">
              Understand any codebase instantly with intelligent AI analysis
            </p>
          </div>

          <div className="glass-card p-6 text-center animate-fadeIn" style={{ animationDelay: '0.4s' }}>
            <div className="p-4 bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-xl w-fit mx-auto mb-4">
              <FaGithub className="text-3xl text-blue-400" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">GitHub Integration</h3>
            <p className="text-white/70">
              Seamlessly connect and analyze any GitHub repository
            </p>
          </div>

          <div className="glass-card p-6 text-center animate-fadeIn" style={{ animationDelay: '0.6s' }}>
            <div className="p-4 bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-xl w-fit mx-auto mb-4">
              <FaChartLine className="text-3xl text-blue-400" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Tech Stack Detection</h3>
            <p className="text-white/70">
              Automatically identify technologies and frameworks used
            </p>
          </div>
        </div>

        {/* Project Description */}
        <div className="glass-card p-8 animate-fadeIn" style={{ animationDelay: '0.8s' }}>
          <h2 className="text-3xl font-bold gradient-text mb-6 text-center">
            About CodeGraph AI
          </h2>
          <div className="space-y-4 text-white/80">
            <p>
              CodeGraph AI is an intelligent developer onboarding assistant that helps you understand
              any GitHub repository quickly and efficiently. Whether you're joining a new team,
              exploring open-source projects, or analyzing codebases, CodeGraph AI provides
              AI-powered insights to accelerate your understanding.
            </p>
            <p>
              Our platform uses advanced machine learning to analyze code structure, detect
              technologies, generate summaries, and provide interactive Q&A capabilities about
              any repository.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
