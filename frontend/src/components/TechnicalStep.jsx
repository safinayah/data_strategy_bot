import { useState } from 'react'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { ChevronRight, ChevronLeft, Settings, X } from 'lucide-react'

const TechnicalStep = ({ formData, updateFormData, nextStep, prevStep }) => {
  const [newCloudProvider, setNewCloudProvider] = useState('')
  const [newDatabase, setNewDatabase] = useState('')

  const techEnvironments = [
    'On-premises',
    'Cloud-native',
    'Hybrid (On-premises + Cloud)',
    'Multi-cloud',
    'Edge computing'
  ]

  const addItem = (field, value, setter) => {
    if (value.trim() && !formData.technical_environment[field].includes(value.trim())) {
      updateFormData('technical_environment', {
        [field]: [...formData.technical_environment[field], value.trim()]
      })
      setter('')
    }
  }

  const removeItem = (field, item) => {
    updateFormData('technical_environment', {
      [field]: formData.technical_environment[field].filter(i => i !== item)
    })
  }

  const isValid = formData.technical_environment.technology_environment

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
            <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
              <Settings className="w-5 h-5 text-orange-600" />
            </div>
            <div>
              <CardTitle className="text-xl">Technical Environment</CardTitle>
              <CardDescription>
                Tell us about your current technology infrastructure and team
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Technology Environment */}
          <div className="space-y-2">
            <Label className="text-sm font-medium">Technology Environment *</Label>
            <Select 
              value={formData.technical_environment.technology_environment} 
              onValueChange={(value) => updateFormData('technical_environment', { technology_environment: value })}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select your technology environment" />
              </SelectTrigger>
              <SelectContent>
                {techEnvironments.map((env) => (
                  <SelectItem key={env} value={env.toLowerCase()}>
                    {env}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Cloud Providers */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">Cloud Providers</Label>
            <p className="text-sm text-gray-600">
              Which cloud platforms do you currently use or plan to use?
            </p>
            <div className="flex space-x-2">
              <Input
                placeholder="Add cloud provider (e.g., AWS, Azure, Google Cloud)"
                value={newCloudProvider}
                onChange={(e) => setNewCloudProvider(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && addItem('cloud_providers', newCloudProvider, setNewCloudProvider)}
                className="flex-1"
              />
              <Button 
                type="button" 
                onClick={() => addItem('cloud_providers', newCloudProvider, setNewCloudProvider)} 
                variant="outline"
              >
                Add
              </Button>
            </div>
            {formData.technical_environment.cloud_providers.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {formData.technical_environment.cloud_providers.map((provider) => (
                  <Badge key={provider} variant="default" className="flex items-center space-x-1 bg-orange-100 text-orange-800 hover:bg-orange-200">
                    <span>{provider}</span>
                    <X 
                      className="w-3 h-3 cursor-pointer hover:text-orange-600" 
                      onClick={() => removeItem('cloud_providers', provider)}
                    />
                  </Badge>
                ))}
              </div>
            )}
          </div>

          {/* Database Technologies */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">Database Technologies</Label>
            <p className="text-sm text-gray-600">
              What database systems and data storage technologies do you use?
            </p>
            <div className="flex space-x-2">
              <Input
                placeholder="Add database (e.g., PostgreSQL, MongoDB, Snowflake)"
                value={newDatabase}
                onChange={(e) => setNewDatabase(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && addItem('database_technologies', newDatabase, setNewDatabase)}
                className="flex-1"
              />
              <Button 
                type="button" 
                onClick={() => addItem('database_technologies', newDatabase, setNewDatabase)} 
                variant="outline"
              >
                Add
              </Button>
            </div>
            {formData.technical_environment.database_technologies.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {formData.technical_environment.database_technologies.map((db) => (
                  <Badge key={db} variant="outline" className="flex items-center space-x-1">
                    <span>{db}</span>
                    <X 
                      className="w-3 h-3 cursor-pointer hover:text-red-500" 
                      onClick={() => removeItem('database_technologies', db)}
                    />
                  </Badge>
                ))}
              </div>
            )}
          </div>

          {/* Technical Team Size */}
          <div className="space-y-2">
            <Label htmlFor="team_size" className="text-sm font-medium">
              Technical Team Size
            </Label>
            <p className="text-sm text-gray-600">
              How many people are in your technical/IT team?
            </p>
            <Input
              id="team_size"
              type="number"
              placeholder="Enter number of team members"
              value={formData.technical_environment.technical_team_size || ''}
              onChange={(e) => updateFormData('technical_environment', { 
                technical_team_size: e.target.value ? parseInt(e.target.value) : null 
              })}
              className="w-full"
              min="0"
            />
          </div>

          {/* Scalability Needs */}
          <div className="space-y-2">
            <Label htmlFor="scalability_needs" className="text-sm font-medium">
              Scalability Needs
            </Label>
            <p className="text-sm text-gray-600">
              What are your expected growth and scalability requirements?
            </p>
            <Input
              id="scalability_needs"
              placeholder="e.g., 50% growth expected, Need to handle 10x more data"
              value={formData.technical_environment.scalability_needs}
              onChange={(e) => updateFormData('technical_environment', { scalability_needs: e.target.value })}
              className="w-full"
            />
          </div>
        </CardContent>
      </Card>

      {/* Technology Examples Card */}
      <Card className="bg-orange-50 border-orange-200">
        <CardHeader>
          <CardTitle className="text-lg text-orange-900">🛠️ Common Technologies</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <h4 className="font-semibold text-orange-800 mb-2">Cloud Providers</h4>
              <ul className="space-y-1 text-orange-700">
                <li>• Amazon Web Services (AWS)</li>
                <li>• Microsoft Azure</li>
                <li>• Google Cloud Platform</li>
                <li>• IBM Cloud</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-orange-800 mb-2">Databases</h4>
              <ul className="space-y-1 text-orange-700">
                <li>• PostgreSQL, MySQL</li>
                <li>• MongoDB, Cassandra</li>
                <li>• Snowflake, BigQuery</li>
                <li>• Oracle, SQL Server</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-orange-800 mb-2">Environments</h4>
              <ul className="space-y-1 text-orange-700">
                <li>• On-premises data centers</li>
                <li>• Public cloud</li>
                <li>• Hybrid cloud</li>
                <li>• Multi-cloud strategy</li>
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

export default TechnicalStep

