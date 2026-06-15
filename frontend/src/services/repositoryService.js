import api from './api'

export const analyzeRepository = async (repoUrl) => {
  const response = await api.post(
    '/repository/analyze',
    {
      repo_url: repoUrl,
    }
  )

  return response.data
}