import { useState, useEffect } from 'react'

const API_BASE_URL = 'http://localhost:8000'

export const useApi = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const apiCall = async (endpoint, options = {}) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }))
        throw new Error(errorData.detail || `HTTP ${response.status}`)
      }

      const data = await response.json()
      return data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const healthCheck = () => apiCall('/health')
  
  const createRecommendation = (organizationalInput, aiModel = 'huggingface') => 
    apiCall('/recommendations', {
      method: 'POST',
      body: JSON.stringify({
        organizational_input: organizationalInput,
        ai_model: aiModel,
        output_format: 'both'
      })
    })

  const getRecommendationStatus = (sessionId) => 
    apiCall(`/recommendations/${sessionId}/status`)

  const getRecommendation = (sessionId) => 
    apiCall(`/recommendations/${sessionId}`)

  const downloadReport = async (sessionId, format = 'markdown', type = 'technical') => {
    const response = await fetch(`${API_BASE_URL}/recommendations/${sessionId}/download?format=${format}&type=${type}`)
    
    if (response.ok) {
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.style.display = 'none'
      a.href = url
      a.download = `data_strategy_${type}_report.${format === 'pdf' ? 'pdf' : 'md'}`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } else {
      throw new Error('Download failed')
    }
  }

  const validateInput = (input) => 
    apiCall('/validate-input', {
      method: 'POST',
      body: JSON.stringify(input)
    })

  return {
    loading,
    error,
    healthCheck,
    createRecommendation,
    getRecommendationStatus,
    getRecommendation,
    downloadReport,
    validateInput
  }
}

export const useRecommendationPolling = (sessionId) => {
  const [status, setStatus] = useState(null)
  const [recommendation, setRecommendation] = useState(null)
  const [error, setError] = useState(null)
  const { getRecommendationStatus, getRecommendation } = useApi()

  useEffect(() => {
    if (!sessionId) return

    const pollStatus = async () => {
      try {
        const statusData = await getRecommendationStatus(sessionId)
        setStatus(statusData)

        if (statusData.status === 'completed') {
          const recData = await getRecommendation(sessionId)
          setRecommendation(recData)
        } else if (statusData.status === 'failed') {
          setError(statusData.error || 'Recommendation generation failed')
        }
      } catch (err) {
        setError(err.message)
      }
    }

    // Poll immediately
    pollStatus()

    // Set up polling interval
    const interval = setInterval(pollStatus, 2000) // Poll every 2 seconds

    return () => clearInterval(interval)
  }, [sessionId])

  return { status, recommendation, error }
}

