import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import './App.css'

// Import components
import WelcomeStep from './components/WelcomeStep'
import ProfileStep from './components/ProfileStep'
import DataLandscapeStep from './components/DataLandscapeStep'
import ObjectivesStep from './components/ObjectivesStep'
import TechnicalStep from './components/TechnicalStep'
import ChallengesStep from './components/ChallengesStep'
import ResultsStep from './components/ResultsStep'

// Import hooks
import { useApi, useRecommendationPolling } from './hooks/useApi'

// Import UI components
import { Progress } from '@/components/ui/progress'
import { Card, CardContent } from '@/components/ui/card'

const STEPS = [
  { id: 'welcome', title: 'Welcome', component: WelcomeStep },
  { id: 'profile', title: 'Company Profile', component: ProfileStep },
  { id: 'data', title: 'Data Landscape', component: DataLandscapeStep },
  { id: 'objectives', title: 'Business Objectives', component: ObjectivesStep },
  { id: 'technical', title: 'Technical Environment', component: TechnicalStep },
  { id: 'challenges', title: 'Current Challenges', component: ChallengesStep },
  { id: 'results', title: 'Your Strategy', component: ResultsStep }
]

function App() {
  const [currentStep, setCurrentStep] = useState(0)
  const [sessionId, setSessionId] = useState(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [apiError, setApiError] = useState(null)
  
  const { createRecommendation, healthCheck, error: apiHookError } = useApi()
  const { status, recommendation, error: pollingError } = useRecommendationPolling(sessionId)

  // Initialize form data
  const [formData, setFormData] = useState({
    profile: {
      company_name: '',
      industry: '',
      company_size: '',
      business_model: '',
      geographic_presence: [],
      regulatory_requirements: []
    },
    data_landscape: {
      primary_data_sources: [],
      data_volume_estimate: '',
      data_types: [],
      current_data_tools: [],
      data_governance_maturity: ''
    },
    business_objectives: {
      strategic_goals: [],
      success_metrics: [],
      timeline: '',
      budget_range: ''
    },
    technical_environment: {
      technology_environment: '',
      cloud_providers: [],
      database_technologies: [],
      technical_team_size: null,
      scalability_needs: ''
    },
    challenges: {
      data_silos: false,
      data_quality_issues: false,
      manual_processes: false,
      reporting_delays: false,
      compliance_risks: false,
      scalability_issues: false,
      skill_gaps: false,
      budget_limitations: false
    }
  })

  // Check API health on mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        await healthCheck()
        console.log('API is healthy')
      } catch (error) {
        console.error('API health check failed:', error)
        setApiError('Unable to connect to the API server. Please ensure the backend is running.')
      }
    }
    
    checkHealth()
  }, [])

  // Handle recommendation status updates
  useEffect(() => {
    if (status) {
      if (status.status === 'completed') {
        setIsGenerating(false)
        setCurrentStep(6) // Move to results step
      } else if (status.status === 'failed') {
        setIsGenerating(false)
        setApiError(status.error || 'Recommendation generation failed')
      }
    }
  }, [status])

  const updateFormData = (section, data) => {
    setFormData(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        ...data
      }
    }))
  }

  const nextStep = () => {
    if (currentStep < STEPS.length - 1) {
      setCurrentStep(currentStep + 1)
    }
  }

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  const generateRecommendations = async () => {
    setIsGenerating(true)
    setApiError(null)
    
    try {
      const response = await createRecommendation(formData, 'huggingface')
      setSessionId(response.session_id)
    } catch (error) {
      setIsGenerating(false)
      setApiError(error.message || 'Failed to start recommendation generation')
    }
  }

  const CurrentStepComponent = STEPS[currentStep].component
  const progress = ((currentStep + 1) / STEPS.length) * 100

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">DS</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Data Strategy Bot</h1>
                <p className="text-sm text-gray-600">AI-Powered DMBOK Recommendations</p>
              </div>
            </div>
            
            {/* Progress indicator */}
            <div className="hidden md:flex items-center space-x-4">
              <span className="text-sm text-gray-600">
                Step {currentStep + 1} of {STEPS.length}
              </span>
              <div className="w-32">
                <Progress value={progress} className="h-2" />
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* API Error Banner */}
      {(apiError || apiHookError || pollingError) && (
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-red-50 border-l-4 border-red-400 p-4"
        >
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">
                  {apiError || apiHookError || pollingError}
                </p>
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          
          {/* Sidebar - Step Navigation */}
          <div className="lg:col-span-1">
            <Card className="sticky top-8">
              <CardContent className="p-6">
                <h3 className="font-semibold text-gray-900 mb-4">Progress</h3>
                <div className="space-y-3">
                  {STEPS.map((step, index) => (
                    <motion.div
                      key={step.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className={`flex items-center space-x-3 p-2 rounded-lg transition-colors ${
                        index === currentStep
                          ? 'bg-blue-100 text-blue-700'
                          : index < currentStep
                          ? 'bg-green-50 text-green-700'
                          : 'text-gray-500'
                      }`}
                    >
                      <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-semibold ${
                        index === currentStep
                          ? 'bg-blue-600 text-white'
                          : index < currentStep
                          ? 'bg-green-600 text-white'
                          : 'bg-gray-300 text-gray-600'
                      }`}>
                        {index < currentStep ? '✓' : index + 1}
                      </div>
                      <span className="text-sm font-medium">{step.title}</span>
                    </motion.div>
                  ))}
                </div>

                {/* Progress Bar for Mobile */}
                <div className="mt-6 md:hidden">
                  <div className="flex justify-between text-sm text-gray-600 mb-2">
                    <span>Progress</span>
                    <span>{Math.round(progress)}%</span>
                  </div>
                  <Progress value={progress} className="h-2" />
                </div>

                {/* Session Info */}
                {sessionId && (
                  <div className="mt-6 p-3 bg-blue-50 rounded-lg">
                    <p className="text-xs text-blue-600 font-medium">Session ID</p>
                    <p className="text-xs text-blue-800 font-mono break-all">{sessionId}</p>
                  </div>
                )}

                {/* Status Info */}
                {status && (
                  <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                    <p className="text-xs text-gray-600 font-medium">Status</p>
                    <p className="text-xs text-gray-800 capitalize">{status.status}</p>
                    {status.progress !== undefined && (
                      <div className="mt-2">
                        <Progress value={status.progress} className="h-1" />
                        <p className="text-xs text-gray-600 mt-1">{status.progress}% complete</p>
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Main Content Area */}
          <div className="lg:col-span-3">
            <AnimatePresence mode="wait">
              <motion.div
                key={currentStep}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
              >
                <CurrentStepComponent
                  formData={formData}
                  updateFormData={updateFormData}
                  nextStep={nextStep}
                  prevStep={prevStep}
                  generateRecommendations={generateRecommendations}
                  isGenerating={isGenerating}
                  error={apiError || apiHookError || pollingError}
                  recommendations={recommendation}
                  sessionId={sessionId}
                />
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-50 border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-sm text-gray-600">
            <p>Powered by DMBOK Framework & AI • Built for Enterprise Data Strategy</p>
            <p className="mt-2">© 2024 Data Strategy Bot. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App

