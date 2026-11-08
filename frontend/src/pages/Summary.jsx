import React from 'react'
import ReactMarkdown from 'react-markdown'
import { useRepository } from '../context/RepositoryContext'

const Summary = () => {
  const { activeRepo } = useRepository()
  const analysis = activeRepo || JSON.parse(localStorage.getItem('lastAnalysis') || 'null')

  if (!analysis) {
    return (
      <div className="p-8">
        <h2 className="text-xl font-semibold text-white mb-4">Repository Summary</h2>
        <div className="text-slate-400">No repository analyzed yet. Please run analysis from Dashboard.</div>
      </div>
    )
  }

  return (
    <div className="p-8 max-w-5xl">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight">
            Repository Summary
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Intelligence overview for <span className="text-blue-400 font-mono font-medium">{analysis.repo_name}</span>
          </p>
        </div>
      </div>

      <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-6 md:p-8 shadow-xl">
        {analysis.summary ? (
          <ReactMarkdown
            components={{
              // Main title (# Developer Onboarding Report)
              h1: ({ children }) => (
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-500 bg-clip-text text-transparent pb-4 border-b border-slate-800 mb-6">
                  {children}
                </h1>
              ),
              // Section headings (## 1. Project Overview, etc.)
              h2: ({ children }) => (
                <h2 className="text-lg font-bold text-slate-100 mt-8 mb-3 pb-2 border-b border-slate-800/80 flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-blue-500 inline-block shadow-sm shadow-blue-500/50"></span>
                  {children}
                </h2>
              ),
              // Subheadings (### Sub-section)
              h3: ({ children }) => (
                <h3 className="text-sm font-semibold uppercase tracking-wider text-indigo-400 mt-5 mb-2">
                  {children}
                </h3>
              ),
              // Paragraphs
              p: ({ children }) => (
                <p className="text-slate-300 text-sm leading-relaxed mb-3">
                  {children}
                </p>
              ),
              // Unordered lists
              ul: ({ children }) => (
                <ul className="space-y-2 mb-4 text-sm text-slate-300 list-disc list-outside ml-4">
                  {children}
                </ul>
              ),
              // Ordered lists (Execution workflow)
              ol: ({ children }) => (
                <ol className="space-y-2.5 mb-4 text-sm text-slate-300 list-decimal list-outside ml-5">
                  {children}
                </ol>
              ),
              // List item
              li: ({ children }) => (
                <li className="leading-relaxed marker:text-slate-500">
                  {children}
                </li>
              ),
              // Strong / Bold labels
              strong: ({ children }) => (
                <strong className="font-semibold text-slate-100">
                  {children}
                </strong>
              ),
              // File paths & commands (`app.py`, `src/predict.py`)
              code: ({ children }) => (
                <code className="text-cyan-300 bg-slate-900 px-1.5 py-0.5 rounded text-[13px] font-mono border border-slate-700/60 shadow-inner">
                  {children}
                </code>
              ),
              // Quotes or Notes
              blockquote: ({ children }) => (
                <blockquote className="border-l-4 border-indigo-500 bg-slate-800/40 px-4 py-2 my-4 rounded-r text-sm text-slate-300 italic">
                  {children}
                </blockquote>
              )
            }}
          >
            {analysis.summary}
          </ReactMarkdown>
        ) : (
          <div className="text-slate-400">No summary available.</div>
        )}
      </div>
    </div>
  )
}

export default Summary