
import React, { useState, useEffect } from "react";
import axios from "axios";
import API_BASE_URL from '../config/api'
import ReactMarkdown from "react-markdown";
import { useRepository } from '../context/RepositoryContext'

// Small helper to render code/file references more clearly inside markdown
const MarkdownComponents = {
  code({ node, inline, className, children, ...props }) {
    return (
      <code className={`bg-white/5 px-1 py-0.5 rounded font-mono text-sm ${inline ? '' : 'block p-2 my-2'}`} {...props}>
        {children}
      </code>
    )
  }
}

const RepositoryChat = ({ repoName, persistedMessages = [] }) => {

  const { addChatMessage, activeRepo } = useRepository()

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState(persistedMessages || []);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Initialize messages from context/persisted only if local state is empty.
    // This prevents overwriting local conversation while user interacts.
    if (activeRepo && Array.isArray(activeRepo.chatMessages) && messages.length === 0) {
      setMessages(activeRepo.chatMessages)
    }
  }, [activeRepo, messages.length])

  const askQuestion = async () => {
    if (!question.trim() || loading) return

    const userQuestion = question.trim()

    const userMsg = { role: 'user', content: userQuestion }

    // Persist the user message immediately to context (storage)
    addChatMessage(userMsg)

    // Locally show user message and a loading assistant placeholder
    const loadingAssistant = { role: 'assistant', content: 'Reporyx-AI is thinking...', loading: true }
    setMessages(prev => [...prev, userMsg, loadingAssistant])

    setQuestion('')
    setLoading(true)

    try {
      // send last few messages as history (exclude our local loading placeholder)
      const historyToSend = messages.slice(-6).concat(userMsg).slice(-6)

      const response = await axios.post(
        `${API_BASE_URL}/chat/ask`,
        {
          question: userQuestion,
          repo_name: repoName,
          history: historyToSend
        }
      )

      const assistantMsg = { role: 'assistant', content: response.data.answer, sources: response.data.sources || [] }

      // Replace the loading assistant placeholder with the real assistant message
      setMessages(prev => {
        const idx = prev.findIndex(m => m.loading)
        if (idx !== -1) {
          const copy = [...prev]
          copy.splice(idx, 1, assistantMsg)
          return copy
        }
        return [...prev, assistantMsg]
      })

      // Persist assistant message
      addChatMessage(assistantMsg)
    } catch (error) {
      const errMsg = { role: 'assistant', content: '❌ Error generating answer. Please try again.' }

      setMessages(prev => {
        const idx = prev.findIndex(m => m.loading)
        if (idx !== -1) {
          const copy = [...prev]
          copy.splice(idx, 1, errMsg)
          return copy
        }
        return [...prev, errMsg]
      })

      addChatMessage(errMsg)
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') askQuestion()
  }

  return (
    <div className="glass-card p-6 mt-6">

      <h2 className="text-xl font-bold text-white mb-4">
        Ask Repository
      </h2>

      <input
        type="text"
        placeholder="Ask anything about this repository..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={handleKeyDown}
        className="input-field"
      />

      <button
        onClick={askQuestion}
        disabled={loading}
        className="btn-primary mt-4"
      >
        {loading
          ? "Thinking..."
          : "Ask"}
      </button>

      <div className="mt-6 flex flex-col gap-4 overflow-x-hidden">
        {messages.map((message, index) => {
          if (message.role === 'user') {
            return (
              <div key={index} className="flex justify-end">
                <div
                  className="max-w-[85%] p-3 rounded-lg text-white bg-gradient-to-r from-blue-600 to-purple-600 shadow-sm"
                  style={{ wordBreak: 'break-word', overflowWrap: 'break-word', whiteSpace: 'pre-wrap' }}
                >
                  <div className="text-xs text-white/80 font-medium">You</div>
                  <div className="mt-1 whitespace-pre-wrap break-words">{message.content}</div>
                </div>
              </div>
            )
          }

          // assistant or loading
          return (
            <div key={index} className="flex justify-start">
              <div
                className="max-w-[85%] bg-[#0b1220] border border-[#1f2937] p-4 rounded-lg text-white shadow-sm"
                style={{ wordBreak: 'break-word', overflowWrap: 'break-word', whiteSpace: 'pre-wrap' }}
              >
                <div className="text-xs text-white/80 font-medium">Reporyx-AI</div>
                <div className="mt-2 prose prose-invert max-w-none break-words whitespace-pre-wrap">
                  <ReactMarkdown components={MarkdownComponents}>{message.content}</ReactMarkdown>
                </div>

                {message.role === 'assistant' && message.sources && message.sources.length > 0 && (
                  <div className="mt-4 border-t border-white/10 pt-3">
                    <p className="text-xs text-gray-400 mb-2">Sources</p>
                    {message.sources.map((source, idx) => (
                      <div key={idx} className="text-sm text-blue-300">📄 {source}</div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )
        })}
      </div>

    </div>
  );
};

export default RepositoryChat;

