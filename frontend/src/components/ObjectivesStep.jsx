import { useState } from 'react'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { ChevronRight, ChevronLeft, Target, X } from 'lucide-react'

const ObjectivesStep = ({ formData, updateFormData, nextStep, prevStep }) => {
  const [newGoal, setNewGoal] = useState('')
  const [newKPI, setNewKPI] = useState('')
  const [newInitiative, setNewInitiative] = useState('')

  const addItem = (field, value, setter) => {
    if (value.trim() && !formData.business_objectives[field].includes(value.trim())) {
      updateFormData('business_objectives', {
        [field]: [...formData.business_objectives[field], value.trim()]
      })
      setter('')
    }
  }

  const removeItem = (field, item) => {
    updateFormData('business_objectives', {
      [field]: formData.business_objectives[field].filter(i => i !== item)
    })
  }

  const isValid = formData.business_objectives.strategic_goals.length > 0

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
            <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
              <Target className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <CardTitle className="text-xl">Business Objectives</CardTitle>
              <CardDescription>
                Define your strategic goals and key performance indicators
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Strategic Goals */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">Strategic Goals *</Label>
            <p className="text-sm text-gray-600">
              What are your organization's main strategic objectives?
            </p>
            <div className="flex space-x-2">
              <Input
                placeholder="Add strategic goal (e.g., Improve customer experience, Reduce costs)"
                value={newGoal}
                onChange={(e) => setNewGoal(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && addItem('strategic_goals', newGoal, setNewGoal)}
                className="flex-1"
              />
              <Button 
                type="button" 
                onClick={() => addItem('strategic_goals', newGoal, setNewGoal)} 
                variant="outline"
              >
                Add
              </Button>
            </div>
            {formData.business_objectives.strategic_goals.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {formData.business_objectives.strategic_goals.map((goal) => (
                  <Badge key={goal} variant="default" className="flex items-center space-x-1 bg-purple-100 text-purple-800 hover:bg-purple-200">
                    <span>{goal}</span>
                    <X 
                      className="w-3 h-3 cursor-pointer hover:text-purple-600" 
                      onClick={() => removeItem('strategic_goals', goal)}
                    />
                  </Badge>
                ))}
              </div>
            )}
          </div>

          {/* Key Performance Indicators */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">Key Performance Indicators (KPIs)</Label>
            <p className="text-sm text-gray-600">
              How do you measure success in your organization?
            </p>
            <div className="flex space-x-2">
              <Input
                placeholder="Add KPI (e.g., Customer satisfaction score, Revenue growth)"
                value={newKPI}
                onChange={(e) => setNewKPI(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && addItem('key_performance_indicators', newKPI, setNewKPI)}
                className="flex-1"
              />
              <Button 
                type="button" 
                onClick={() => addItem('key_performance_indicators', newKPI, setNewKPI)} 
                variant="outline"
              >
                Add
              </Button>
            </div>
            {formData.business_objectives.key_performance_indicators.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {formData.business_objectives.key_performance_indicators.map((kpi) => (
                  <Badge key={kpi} variant="outline" className="flex items-center space-x-1">
                    <span>{kpi}</span>
                    <X 
                      className="w-3 h-3 cursor-pointer hover:text-red-500" 
                      onClick={() => removeItem('key_performance_indicators', kpi)}
                    />
                  </Badge>
                ))}
              </div>
            )}
          </div>

          {/* Digital Transformation Initiatives */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">Digital Transformation Initiatives</Label>
            <p className="text-sm text-gray-600">
              What digital transformation projects are you planning or implementing?
            </p>
            <div className="flex space-x-2">
              <Input
                placeholder="Add initiative (e.g., AI implementation, Cloud migration)"
                value={newInitiative}
                onChange={(e) => setNewInitiative(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && addItem('digital_transformation_initiatives', newInitiative, setNewInitiative)}
                className="flex-1"
              />
              <Button 
                type="button" 
                onClick={() => addItem('digital_transformation_initiatives', newInitiative, setNewInitiative)} 
                variant="outline"
              >
                Add
              </Button>
            </div>
            {formData.business_objectives.digital_transformation_initiatives.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {formData.business_objectives.digital_transformation_initiatives.map((initiative) => (
                  <Badge key={initiative} variant="secondary" className="flex items-center space-x-1">
                    <span>{initiative}</span>
                    <X 
                      className="w-3 h-3 cursor-pointer hover:text-red-500" 
                      onClick={() => removeItem('digital_transformation_initiatives', initiative)}
                    />
                  </Badge>
                ))}
              </div>
            )}
          </div>

          {/* Budget Constraints */}
          <div className="space-y-2">
            <Label htmlFor="budget_constraints" className="text-sm font-medium">
              Budget Constraints
            </Label>
            <p className="text-sm text-gray-600">
              What is your approximate annual budget for data initiatives?
            </p>
            <Input
              id="budget_constraints"
              placeholder="e.g., $100K annually, $500K for this project, Limited budget"
              value={formData.business_objectives.budget_constraints}
              onChange={(e) => updateFormData('business_objectives', { budget_constraints: e.target.value })}
              className="w-full"
            />
          </div>
        </CardContent>
      </Card>

      {/* Quick Examples Card */}
      <Card className="bg-blue-50 border-blue-200">
        <CardHeader>
          <CardTitle className="text-lg text-blue-900">💡 Example Objectives</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <h4 className="font-semibold text-blue-800 mb-2">Strategic Goals</h4>
              <ul className="space-y-1 text-blue-700">
                <li>• Improve customer experience</li>
                <li>• Increase operational efficiency</li>
                <li>• Drive data-driven decisions</li>
                <li>• Enhance competitive advantage</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-blue-800 mb-2">KPIs</h4>
              <ul className="space-y-1 text-blue-700">
                <li>• Customer satisfaction score</li>
                <li>• Time to market</li>
                <li>• Revenue per customer</li>
                <li>• Data quality metrics</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-blue-800 mb-2">Initiatives</h4>
              <ul className="space-y-1 text-blue-700">
                <li>• AI/ML implementation</li>
                <li>• Real-time analytics</li>
                <li>• Data lake modernization</li>
                <li>• Self-service BI</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Navigation */}
      <div className="flex justify-between">
        <Button variant="outline" onClick={prevStep}>
          <ChevronLeft className="mr-2 w-4 h-4" />
          Previous
        </Button>
        <Button 
          onClick={nextStep} 
          disabled={!isValid}
          className="bg-blue-600 hover:bg-blue-700"
        >
          Next Step
          <ChevronRight className="ml-2 w-4 h-4" />
        </Button>
      </div>
    </motion.div>
  )
}

export default ObjectivesStep

