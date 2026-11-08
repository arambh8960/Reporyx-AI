import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import API_BASE_URL from "../config/api";
import ReactMarkdown from "react-markdown";
import { useRepository } from "../context/RepositoryContext";

const MarkdownComponents = {
  // Accurately distinguish inline code spans from multiline code blocks
  code({ node, inline, className, children, ...props }) {
    const isBlockCode = !inline && String(children).includes("\n");

    if (!isBlockCode) {
      return (
        <code
          className="bg-white/10 text-cyan-300 font-mono text-xs px-1.5 py-0.5 rounded mx-0.5 border border-white/5 inline-block"
          {...props}
        >
          {children}
        </code>
      );
    }

    return (
      <div className="my-3 rounded-lg overflow-hidden border border-white/10 bg-black/40">
        <pre className="p-3 text-xs font-mono overflow-x-auto text-gray-200">
          <code className={className} {...props}>
            {children}
          </code>
        </pre>
      </div>
    );
  },
  // Keep paragraphs flowing naturally without artificial line breaks
  p({ children }) {
    return <p className="mb-2 leading-relaxed text-gray-200 text-sm last:mb-0">{children}</p>;
  },
  ul({ children }) {
    return <ul className="list-disc list-inside mb-2 space-y-1 text-sm text-gray-200">{children}</ul>;
  },
  ol({ children }) {
    return <ol className="list-decimal list-inside mb-2 space-y-1 text-sm text-gray-200">{children}</ol>;
  }
};

const RepositoryChat = ({ repoName, persistedMessages = [] }) => {
  const { addChatMessage, activeRepo } = useRepository();

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState(persistedMessages || []);
  const [loading, setLoading] = useState(false);
  const chatBottomRef = useRef(null);

  useEffect(() => {
    if (activeRepo && Array.isArray(activeRepo.chatMessages) && messages.length === 0) {
      setMessages(activeRepo.chatMessages);
    }
  }, [activeRepo, messages.length]);

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const askQuestion = async () => {
    if (!question.trim() || loading) return;

    const userQuestion = question.trim();
    const userMsg = { role: "user", content: userQuestion };

    addChatMessage(userMsg);

    const loadingAssistant = { role: "assistant", content: "Reporyx-AI is thinking...", loading: true };
    setMessages((prev) => [...prev, userMsg, loadingAssistant]);
    setQuestion("");
    setLoading(true);

    try {
      const historyToSend = messages.slice(-6).concat(userMsg).slice(-6);

      const response = await axios.post(`${API_BASE_URL}/chat/ask`, {
        question: userQuestion,
        repo_name: repoName,
        history: historyToSend,
      });

      const assistantMsg = {
        role: "assistant",
        content: response.data.answer,
        sources: response.data.sources || [],
      };

      setMessages((prev) => {
        const idx = prev.findIndex((m) => m.loading);
        if (idx !== -1) {
          const copy = [...prev];
          copy.splice(idx, 1, assistantMsg);
          return copy;
        }
        return [...prev, assistantMsg];
      });

      addChatMessage(assistantMsg);
    } catch (error) {
      const errMsg = { role: "assistant", content: "❌ Error generating answer. Please try again." };

      setMessages((prev) => {
        const idx = prev.findIndex((m) => m.loading);
        if (idx !== -1) {
          const copy = [...prev];
          copy.splice(idx, 1, errMsg);
          return copy;
        }
        return [...prev, errMsg];
      });

      addChatMessage(errMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      askQuestion();
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] max-w-5xl mx-auto rounded-xl border border-white/10 bg-[#0b0f19] shadow-xl overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 border-b border-white/10 bg-white/[0.02] flex items-center justify-between">
        <div>
          <h2 className="text-base font-semibold text-white">Ask Repository</h2>
          <p className="text-xs text-gray-400">Context: {repoName || "Current Workspace"}</p>
        </div>
      </div>

      {/* Messages Stream */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 && (
          <div className="h-full flex items-center justify-center text-gray-500 text-sm">
            Ask any question to inspect code, dependencies, or architectural flows.
          </div>
        )}

        {messages.map((message, index) => {
          if (message.role === "user") {
            return (
              <div key={index} className="flex justify-end">
                <div className="max-w-[80%] px-4 py-2.5 rounded-2xl rounded-tr-sm text-white bg-gradient-to-r from-blue-600 to-indigo-600 shadow-md">
                  <div className="text-[11px] text-white/70 font-medium mb-1">You</div>
                  <div className="text-sm whitespace-pre-wrap break-words leading-relaxed">
                    {message.content}
                  </div>
                </div>
              </div>
            );
          }

          return (
            <div key={index} className="flex justify-start">
              <div className="max-w-[85%] bg-[#111827]/90 border border-white/10 p-4 rounded-2xl rounded-tl-sm text-gray-100 shadow-md">
                <div className="text-[11px] text-purple-400 font-semibold tracking-wide uppercase mb-2 flex items-center gap-1.5">
                  <span className="inline-block w-1.5 h-1.5 rounded-full bg-purple-400"></span>
                  Reporyx-AI
                </div>

                {message.loading ? (
                  <div className="text-sm text-gray-400 italic animate-pulse">
                    {message.content}
                  </div>
                ) : (
                  <div className="break-words">
                    <ReactMarkdown components={MarkdownComponents}>
                      {message.content}
                    </ReactMarkdown>
                  </div>
                )}

                {message.role === "assistant" && message.sources && message.sources.length > 0 && (
                  <div className="mt-4 pt-3 border-t border-white/10">
                    <p className="text-[11px] uppercase tracking-wider font-semibold text-gray-400 mb-2">Sources</p>
                    <div className="flex flex-wrap gap-2">
                      {message.sources.map((source, idx) => (
                        <span
                          key={idx}
                          className="inline-flex items-center gap-1.5 text-xs bg-blue-500/10 border border-blue-500/20 text-blue-300 px-2 py-1 rounded-md font-mono"
                        >
                          📄 {source}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          );
        })}
        <div ref={chatBottomRef} />
      </div>

      {/* Input Form Box */}
      <div className="p-4 border-t border-white/10 bg-[#0d1322]">
        <div className="flex gap-2 items-center">
          <input
            type="text"
            placeholder="Ask anything about this repository..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
            className="flex-1 bg-[#1e293b]/70 border border-white/10 rounded-lg px-4 py-2.5 text-sm text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          />
          <button
            onClick={askQuestion}
            disabled={loading || !question.trim()}
            className="px-5 py-2.5 rounded-lg text-sm font-medium text-white bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-md shadow-blue-600/20"
          >
            {loading ? "Thinking..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default RepositoryChat;