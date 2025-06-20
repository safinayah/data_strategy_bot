import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Checkbox } from '@/components/ui/checkbox.jsx'
import { ChevronRight, ChevronLeft, AlertTriangle } from 'lucide-react'

const ChallengesStep = ({ formData, updateFormData, nextStep, prevStep, generateRecommendations, isGenerating, error }) => {
  const challenges = [
    {
      key: 'data_silos',
      title: 'Data Silos',
      description: 'Data is isolated in different systems and departments'
    },
    {
      key: 'data_quality_issues',
      title: 'Data Quality Issues',
      description: 'Inconsistent, incomplete, or inaccurate data'
    },
    {
      key: 'manual_processes',
      title: 'Manual Processes',
      description: 'Heavy reliance on manual data processing and reporting'
    },
    {
      key: 'reporting_delays',
      title: 'Reporting Delays',
      description: 'Slow or delayed access to business insights'
    },
    {
      key: 'compliance_risks',
      title: 'Compliance Risks',
      description: 'Difficulty meeting regulatory requirements'
    },
    {
      key: 'scalability_issues',
      title: 'Scalability Issues',
      description: 'Current systems cannot handle growing data volumes'
    },
    {
      key: 'skill_gaps',
      title: 'Skill Gaps',
      description: 'Lack of data expertise in the organization'
    },
    {
      key: 'budget_limitations',
      title: 'Budget Limitations',
      description: 'Limited resources for data initiatives'
    }
  ]

  const handleChallengeChange = (challengeKey, checked) => {
    updateFormData('challenges', {
      [challengeKey]: checked
    })
  }

  const selectedChallenges = Object.values(formData.challenges).filter(Boolean).length
  const isValid = selectedChallenges > 0

  const handleGenerateRecommendations = () => {
    generateRecommendations()
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      <Card>
        <CardHeader>
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-red-600" />
            </div>
            <div>
              <CardTitle className="text-xl">Current Challenges</CardTitle>
              <CardDescription>
                Identify the key data-related challenges your organization faces
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-4">
            <Label className="text-sm font-medium">
              Select all challenges that apply to your organization *
            </Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {challenges.map((challenge) => (
                <motion.div
                  key={challenge.key}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.1 * challenges.indexOf(challenge) }}
                  className={`p-4 rounded-lg border-2 transition-all cursor-pointer ${
                    formData.challenges[challenge.key]
                      ? 'border-red-200 bg-red-50'
                      : 'border-gray-200 bg-white hover:border-gray-300'
                  }`}
                  onClick={() => handleChallengeChange(challenge.key, !formData.challenges[challenge.key])}
                >
                  <div className="flex items-start space-x-3">
                    <Checkbox
                      checked={formData.challenges[challenge.key]}
                      onCheckedChange={(checked) => handleChallengeChange(challenge.key, checked)}
                      className="mt-1"
                    />
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900 mb-1">
                        {challenge.title}
                      </h3>
                      <p className="text-sm text-gray-600">
                        {challenge.description}
                      </p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {selectedChallenges > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="p-4 bg-blue-50 border border-blue-200 rounded-lg"
            >
              <p className="text-sm text-blue-800">
                <strong>{selectedChallenges}</strong> challenge{selectedChallenges !== 1 ? 's' : ''} selected. 
                Our AI will generate targeted recommendations to address these specific issues.
              </p>
            </motion.div>
          )}

          {error && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="p-4 bg-red-50 border border-red-200 rounded-lg"
            >
              <p className="text-sm text-red-800">
                <strong>Error:</strong> {error}
              </p>
            </motion.div>
          )}
        </CardContent>
      </Card>

      {/* Summary Card */}
      <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
        <CardHeader>
          <CardTitle className="text-lg text-blue-900">🎯 Ready to Generate Your Strategy</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <p className="text-blue-800">
              Based on your responses, we'll generate a comprehensive data strategy that includes:
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div className="space-y-2">
                <h4 className="font-semibold text-blue-800">📊 Technical Recommendations</h4>
                <ul className="space-y-1 text-blue-700">
                  <li>• DMBOK-based framework analysis</li>
                  <li>• Technology stack recommendations</li>
                  <li>• Implementation roadmap</li>
                  <li>• Risk assessment and mitigation</li>
                </ul>
              </div>
              <div className="space-y-2">
                <h4 className="font-semibold text-blue-800">💼 Executive Summary</h4>
                <ul className="space-y-1 text-blue-700">
                  <li>• ROI analysis and business case</li>
                  <li>• 90-day action plan</li>
                  <li>• Resource requirements</li>
                  <li>• Success metrics and KPIs</li>
                </ul>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Navigation */}
      <div className="flex justify-between">
        <Button variant="outline" onClick={prevStep} disabled={isGenerating}>
          <ChevronLeft className="mr-2 w-4 h-4" />
          Previous
        </Button>
        <Button 
          onClick={handleGenerateRecommendations}
          disabled={!isValid || isGenerating}
          className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-8"
        >
          {isGenerating ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Generating Strategy...
            </>
          ) : (
            <>
              Generate My Data Strategy
              <ChevronRight className="ml-2 w-4 h-4" />
            </>
          )}
        </Button>
      </div>
    </motion.div>
  )
}

export default ChallengesStep

