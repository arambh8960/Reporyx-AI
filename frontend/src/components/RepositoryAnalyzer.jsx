import React, { useState } from 'react'
import { analyzeRepository } from '../services/repositoryService'

const RepositoryAnalyzer = () => {
  const [repoUrl, setRepoUrl] = useState('')
  const [result, setResult] = useState(null)

  const handleAnalyze = async () => {
    try {
      const response = await analyzeRepository(repoUrl)

      setResult(response)
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div className="glass-card p-6">
      <h2 className="text-xl font-bold text-white mb-4">
        Analyze Repository
      </h2>

      <input
        type="text"
        placeholder="https://github.com/facebook/react"
        value={repoUrl}
        onChange={(e) => setRepoUrl(e.target.value)}
        className="input-field"
      />

      <button
        onClick={handleAnalyze}
        className="btn-primary mt-4"
      >
        Analyze Repository
      </button>

      {result && (
        <div className="mt-6 text-white">
          <p>
            <strong>Status:</strong> {result.status}
          </p>

          <p>
            <strong>Repository:</strong> {result.repo_name}
          </p>

          <p>
            <strong>Message:</strong> {result.message}
          </p>
        </div>
      )}
    </div>
  )
}

export default RepositoryAnalyzer