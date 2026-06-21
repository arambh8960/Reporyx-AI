// Centralized API base URL for the frontend.
// Use VITE_API_BASE_URL in environment (.env) for deployments.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default API_BASE_URL
