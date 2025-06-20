import { useState } from 'react'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { 
  CheckCircle, 
  Download, 
  FileText, 
  BarChart3, 
  Target, 
  DollarSign,
  Clock,
  Users,
  Shield,
  TrendingUp,
  AlertTriangle,
  Lightbulb
} from 'lucide-react'

const API_BASE_URL = 'http://localhost:8000'

const ResultsStep = ({ recommendations, sessionId, formData }) => {
  const [downloadingTechnical, setDownloadingTechnical] = useState(false)
  const [downloadingExecutive, setDownloadingExecutive] = useState(false)

  const downloadReport = async (format, type) => {
    if (!sessionId) return
    
    const setLoading = type === 'technical' ? setDownloadingTechnical : setDownloadingExecutive
    setLoading(true)
    
    try {
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
      } else {
        console.error('Download failed')
      }
    } catch (error) {
      console.error('Download error:', error)
    } finally {
      setLoading(false)
    }
  }

  if (!recommendations) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center py-12"
      >
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Generating Your Data Strategy</h3>
        <p className="text-gray-600">This may take a few minutes...</p>
      </motion.div>
    )
  }

  // Mock data structure for demonstration
  const mockMetrics = {
    current_maturity: 6.2,
    target_maturity: 8.5,
    investment_min: 450000,
    investment_max: 650000,
    expected_roi: 280,
    roi_timeframe: 18,
    quick_wins: 5,
    risk_level: 'Medium'
  }

  const mockPriorityRecommendations = [
    {
      title: 'Data Governance Framework',
      priority: 'Critical',
      description: 'Establish comprehensive data governance policies and procedures',
      timeline: '3-6 months',
      investment: '$75K - $125K'
    },
    {
      title: 'Data Quality Management',
      priority: 'High',
      description: 'Implement automated data quality monitoring and remediation',
      timeline: '2-4 months',
      investment: '$50K - $85K'
    },
    {
      title: 'Master Data Management',
      priority: 'High',
      description: 'Create unified customer and product data repositories',
      timeline: '4-8 months',
      investment: '$100K - $150K'
    }
  ]

  const mockActionPlan = [
    {
      phase: 'Phase 1: Foundation (Days 1-30)',
      items: [
        'Conduct comprehensive data audit',
        'Form Data Governance Council',
        'Define data quality baseline metrics',
        'Implement basic data cataloging'
      ]
    },
    {
      phase: 'Phase 2: Quick Wins (Days 31-90)',
      items: [
        'Deploy data quality monitoring tools',
        'Establish data steward roles',
        'Create data dictionary',
        'Implement access controls'
      ]
    },
    {
      phase: 'Phase 3: Strategic Implementation (Days 91-180)',
      items: [
        'Deploy master data management platform',
        'Implement advanced analytics capabilities',
        'Establish self-service BI',
        'Create data literacy training program'
      ]
    }
  ]

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      {/* Success Header */}
      <Card className="border-0 shadow-lg bg-gradient-to-r from-green-600 to-blue-600 text-white">
        <CardHeader className="text-center">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="w-16 h-16 bg-white bg-opacity-20 rounded-full flex items-center justify-center mx-auto mb-4"
          >
            <CheckCircle className="w-8 h-8" />
          </motion.div>
          <CardTitle className="text-2xl font-bold mb-2">
            Your Data Strategy is Ready!
          </CardTitle>
          <CardDescription className="text-green-100 text-lg">
            We've generated a comprehensive, AI-powered data strategy tailored to {formData.profile.company_name || 'your organization'}
          </CardDescription>
        </CardHeader>
      </Card>

      {/* Executive Dashboard */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <BarChart3 className="w-5 h-5 text-blue-600" />
            <span>Executive Dashboard</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{mockMetrics.current_maturity}/10</div>
              <div className="text-sm text-gray-600">Current Maturity</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{mockMetrics.target_maturity}/10</div>
              <div className="text-sm text-gray-600">Target Maturity</div>
            </div>
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">{mockMetrics.expected_roi}%</div>
              <div className="text-sm text-gray-600">Expected ROI</div>
            </div>
            <div className="text-center p-4 bg-orange-50 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">{mockMetrics.quick_wins}</div>
              <div className="text-sm text-gray-600">Quick Wins</div>
            </div>
          </div>
          
          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <div className="flex justify-between items-center mb-2">
              <span className="font-semibold">Investment Required:</span>
              <span className="text-lg font-bold text-blue-600">
                ${mockMetrics.investment_min.toLocaleString()} - ${mockMetrics.investment_max.toLocaleString()}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="font-semibold">Risk Level:</span>
              <Badge variant="outline" className="text-orange-600 border-orange-300">
                {mockMetrics.risk_level}
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Detailed Results Tabs */}
      <Card>
        <CardContent className="p-0">
          <Tabs defaultValue="recommendations" className="w-full">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="recommendations">Recommendations</TabsTrigger>
              <TabsTrigger value="action-plan">Action Plan</TabsTrigger>
              <TabsTrigger value="roi-analysis">ROI Analysis</TabsTrigger>
              <TabsTrigger value="downloads">Downloads</TabsTrigger>
            </TabsList>
            
            <TabsContent value="recommendations" className="p-6 space-y-4">
              <h3 className="text-lg font-semibold mb-4">Priority Recommendations</h3>
              {mockPriorityRecommendations.map((rec, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="border rounded-lg p-4"
                >
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-semibold text-gray-900">{rec.title}</h4>
                    <Badge variant={rec.priority === 'Critical' ? 'destructive' : 'default'}>
                      {rec.priority}
                    </Badge>
                  </div>
                  <p className="text-gray-600 mb-3">{rec.description}</p>
                  <div className="flex space-x-4 text-sm text-gray-500">
                    <div className="flex items-center space-x-1">
                      <Clock className="w-4 h-4" />
                      <span>{rec.timeline}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <DollarSign className="w-4 h-4" />
                      <span>{rec.investment}</span>
                    </div>
                  </div>
                </motion.div>
              ))}
            </TabsContent>
            
            <TabsContent value="action-plan" className="p-6 space-y-4">
              <h3 className="text-lg font-semibold mb-4">90-Day Implementation Plan</h3>
              {mockActionPlan.map((phase, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="border rounded-lg p-4"
                >
                  <h4 className="font-semibold text-gray-900 mb-3">{phase.phase}</h4>
                  <ul className="space-y-2">
                    {phase.items.map((item, itemIndex) => (
                      <li key={itemIndex} className="flex items-center space-x-2">
                        <CheckCircle className="w-4 h-4 text-green-600" />
                        <span className="text-gray-700">{item}</span>
                      </li>
                    ))}
                  </ul>
                </motion.div>
              ))}
            </TabsContent>
            
            <TabsContent value="roi-analysis" className="p-6">
              <h3 className="text-lg font-semibold mb-4">Return on Investment Analysis</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h4 className="font-semibold text-gray-900">Expected Benefits</h4>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span>Operational Efficiency Gains</span>
                      <span className="font-semibold text-green-600">$275K/year</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Improved Decision Making</span>
                      <span className="font-semibold text-green-600">$150K/year</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Risk Reduction</span>
                      <span className="font-semibold text-green-600">$100K/year</span>
                    </div>
                    <div className="flex justify-between border-t pt-2">
                      <span className="font-semibold">Total Annual Benefits</span>
                      <span className="font-bold text-green-600">$525K/year</span>
                    </div>
                  </div>
                </div>
                <div className="space-y-4">
                  <h4 className="font-semibold text-gray-900">Investment Breakdown</h4>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span>Technology & Tools</span>
                      <span className="font-semibold">$350K</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Implementation Services</span>
                      <span className="font-semibold">$200K</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Training & Change Management</span>
                      <span className="font-semibold">$100K</span>
                    </div>
                    <div className="flex justify-between border-t pt-2">
                      <span className="font-semibold">Total Investment</span>
                      <span className="font-bold">$650K</span>
                    </div>
                  </div>
                </div>
              </div>
            </TabsContent>
            
            <TabsContent value="downloads" className="p-6">
              <h3 className="text-lg font-semibold mb-4">Download Your Reports</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <FileText className="w-5 h-5 text-blue-600" />
                      <span>Technical Report</span>
                    </CardTitle>
                    <CardDescription>
                      Detailed technical recommendations for IT teams
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <ul className="text-sm text-gray-600 space-y-1">
                      <li>• DMBOK framework analysis</li>
                      <li>• Technology recommendations</li>
                      <li>• Implementation roadmap</li>
                      <li>• Technical specifications</li>
                    </ul>
                    <div className="flex space-x-2">
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => downloadReport('markdown', 'technical')}
                        disabled={downloadingTechnical}
                      >
                        {downloadingTechnical ? (
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
                        ) : (
                          <Download className="w-4 h-4 mr-2" />
                        )}
                        Markdown
                      </Button>
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => downloadReport('pdf', 'technical')}
                        disabled={downloadingTechnical}
                      >
                        {downloadingTechnical ? (
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
                        ) : (
                          <Download className="w-4 h-4 mr-2" />
                        )}
                        PDF
                      </Button>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <BarChart3 className="w-5 h-5 text-green-600" />
                      <span>Executive Report</span>
                    </CardTitle>
                    <CardDescription>
                      Business-focused summary for leadership
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <ul className="text-sm text-gray-600 space-y-1">
                      <li>• Executive dashboard</li>
                      <li>• ROI analysis & business case</li>
                      <li>• 90-day action plan</li>
                      <li>• Risk assessment</li>
                    </ul>
                    <div className="flex space-x-2">
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => downloadReport('markdown', 'executive')}
                        disabled={downloadingExecutive}
                      >
                        {downloadingExecutive ? (
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-green-600 mr-2"></div>
                        ) : (
                          <Download className="w-4 h-4 mr-2" />
                        )}
                        Markdown
                      </Button>
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => downloadReport('pdf', 'executive')}
                        disabled={downloadingExecutive}
                      >
                        {downloadingExecutive ? (
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-green-600 mr-2"></div>
                        ) : (
                          <Download className="w-4 h-4 mr-2" />
                        )}
                        PDF
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {/* Next Steps */}
      <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
        <CardHeader>
          <CardTitle className="text-lg text-blue-900 flex items-center space-x-2">
            <Lightbulb className="w-5 h-5" />
            <span>Next Steps</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3 text-blue-800">
            <p>🎯 <strong>Share with stakeholders:</strong> Download and present the executive report to leadership</p>
            <p>🛠️ <strong>Technical planning:</strong> Use the technical report to plan implementation details</p>
            <p>📅 <strong>Schedule kickoff:</strong> Begin with Phase 1 activities within the next 30 days</p>
            <p>📊 <strong>Track progress:</strong> Monitor KPIs and adjust strategy as needed</p>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}

export default ResultsStep

