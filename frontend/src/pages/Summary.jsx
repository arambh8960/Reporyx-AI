import React from 'react'
import ReactMarkdown from 'react-markdown'
import { useRepository } from '../context/RepositoryContext'

const StyledHeading = ({ children }) => (
  <h3 className="text-xl md:text-[1.25rem] font-bold mt-6 mb-3 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
    {children}
  </h3>
)

const HEADINGS = [
  'PROJECT OVERVIEW',
  'TECH STACK',
  'CORE FEATURES',
  'HOW IT WORKS',
  'REPOSITORY STRUCTURE INSIGHTS',
  'DEVELOPER ONBOARDING GUIDE',
  'POTENTIAL USE CASES',
  'COMPLEXITY ASSESSMENT',
]

function renderSummaryBlocks(text) {
  if (!text) return []
  const lines = text.split(/\r?\n/)
  const blocks = []
  let buffer = []
  let skippingStructure = false

  function flushBuffer() {
    if (buffer.length === 0) return
    const joined = buffer.join('\n').trim()
    if (joined) blocks.push({ type: 'paragraph', content: joined })
    buffer = []
  }

  for (let rawLine of lines) {
    const line = rawLine.replace(/\t/g, ' ').replace(/\s+$/g, '')
    const trimmed = line.trim()

    const isHeadingLine = trimmed.startsWith('# ')
    const headingText = isHeadingLine ? trimmed.slice(2).trim().toUpperCase() : null

    if (isHeadingLine && HEADINGS.includes(headingText)) {
      // If this is the repository structure heading, enter skip mode
      if (headingText === 'REPOSITORY STRUCTURE INSIGHTS') {
        flushBuffer()
        skippingStructure = true
        continue
      }

      // If we were skipping structure and now hit a new heading, stop skipping
      if (skippingStructure) skippingStructure = false

      flushBuffer()
      blocks.push({ type: 'heading', content: headingText })
      continue
    }

    if (skippingStructure) {
      // skip all lines until the next recognized heading
      continue
    }

    // normal text line - collect
    buffer.push(line)
  }

  flushBuffer()
  return blocks
}
const Summary = () => {
  const { activeRepo } = useRepository()
  const analysis = activeRepo || JSON.parse(localStorage.getItem('lastAnalysis') || 'null')

  if (!analysis) {
    return (
      <div className="p-8">
        <h2 className="text-xl font-semibold text-white mb-4">Repository Summary</h2>
        <div className="text-white">No repository analyzed yet. Please run analysis from Dashboard.</div>
      </div>
    )
  }

  return (
    <div className="p-8">
      <h2 className="text-2xl font-semibold text-white mb-6">Repository Summary — {analysis.repo_name}</h2>

      <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-6">
        {analysis.summary ? (
          (() => {
            const blocks = renderSummaryBlocks(analysis.summary)
            return blocks.map((b, idx) => {
              if (b.type === 'heading') {
                return (
                  <div key={idx}>
                    <h3 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent mt-6 mb-3 uppercase">
                      {b.content}
                    </h3>
                  </div>
                )
              }
              return (
                <div key={idx} className="mt-2 text-white/70">
                  <ReactMarkdown>{b.content}</ReactMarkdown>
                </div>
              )
            })
          })()
        ) : (
          <div className="mt-2 text-white/70">No summary available.</div>
        )}
      </div>
    </div>
  )
}

export default Summary
