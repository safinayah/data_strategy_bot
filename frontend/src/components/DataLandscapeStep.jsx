import { useState } from 'react'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Checkbox } from '@/components/ui/checkbox.jsx'
import { ChevronRight, ChevronLeft, Database, X } from 'lucide-react'

const DataLandscapeStep = ({ formData, updateFormData, nextStep, prevStep }) => {
  const [newDataSource, setNewDataSource] = useState('')
  const [newDataType, setNewDataType] = useState('')
  const [newTool, setNewTool] = useState('')
  const [newQualityIssue, setNewQualityIssue] = useState('')
  const [newComplianceChallenge, setNewComplianceChallenge] = useState('')

  const dataVolumes = [
    'Less than 1TB',
    '1TB - 10TB',
    '10TB - 100TB',
    '100TB - 1PB',
    'More than 1PB',
    'Unknown'
  ]

  const maturityLevels = [
    'ad_hoc',
    'developing', 
    'managed',
    'optimized'
  ]

  const maturityLabels = {
    'ad_hoc': 'Ad Hoc - Minimal governance',
    'developing': 'Developing - Basic policies in place',
    'managed': 'Managed - Formal governance structure',
    'optimized': 'Optimized - Advanced, automated governance'
  }

  const addItem = (field, value, setter) => {
    if (value.trim() && !formData.data_landscape[field].includes(value.trim())) {
      updateFormData('data_landscape', {
        [field]: [...formData.data_landscape[field], value.trim()]
      })
      setter('')
    }
  }

  const removeItem = (field, item) => {
    updateFormData('data_landscape', {
      [field]: formData.data_landscape[field].filter(i => i !== item)
    })
  }

  const isValid = formData.data_landscape.primary_data_sources.length > 0 && 
                  formData.data_landscape.data_volume_estimate

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
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <Database className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <CardTitle className="text-xl">Data Landscape</CardTitle>
              <CardDescription>
                Describe your current data environment and infrastructure
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Primary Data Sources */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">Primary Data Sources *</Label>
            <div className="flex space-x-2">
              <Input
                placeholder="Add data source (e.g., CRM, ERP, Website)"
                value={newDataSource}
                onChange={(e) => setNewDataSource(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && addItem('primary_data_sources', newDataSource, setNewDataSource)}
                className="flex-1"
              />
              <Button 
                type="button" 
                onClick={() => addItem('primary_data_sources', newDataSource, setNewDataSource)} 
                variant="outline"
              >
                Add
              </Button>
            </div>
            {formData.data_landscape.primary_data_sources.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {formData.data_landscape.primary_data_sources.map((source) => (
                  <Badge key={source} variant="secondary" className="flex items-center space-x-1">
                    <span>{source}</span>
                    <X 
                      className="w-3 h-3 cursor-pointer hover:text-red-500" 
                      onClick={() => removeItem('primary_data_sources', source)}
                    />
                  </Badge>
                ))}
              </div>
            )}
          </div>

          {/* Data Volume Estimate */}
          <div className="space-y-2">
            <Label className="text-sm font-medium">Data Volume Estimate *</Label>
            <Select 
              value={formData.data_landscape.data_volume_estimate} 
              onValueChange={(value) => updateFormData('data_landscape', { data_volume_estimate: value })}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select approximate data volume" />
              </SelectTrigger>
              <SelectContent>
                {dataVolumes.map((volume) => (
                  <SelectItem key={volume} value={volume.toLowerCase()}>
                    {volume}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Data Types */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">Data Types</Label>
            <div className="flex space-x-2">
              <Input
                placeholder="Add data type (e.g., Customer, Financial, Operational)"
                value={newDataType}
                onChange={(e) => setNewDataType(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && addItem('data_types', newDataType, setNewDataType)}
                className="flex-1"
              />
              <Button 
                type="button" 
                onClick={() => addItem('data_types', newDataType, setNewDataType)} 
                variant="outline"
              >
                Add
              </Button>
            </div>
            {formData.data_landscape.data_types.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {formData.data_landscape.data_types.map((type) => (
                  <Badge key={type} variant="outline" className="flex items-center space-x-1">
                    <span>{type}</span>
                    <X 
                      className="w-3 h-3 cursor-pointer hover:text-red-500" 
                      onClick={() => removeItem('data_types', type)}
                    />
                  </Badge>
                ))}
              </div>
            )}
          </div>

          {/* Current Data Tools */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">Current Data Tools</Label>
            <div className="flex space-x-2">
              <Input
                placeholder="Add tool (e.g., Tableau, Power BI, Snowflake)"
                value={newTool}
                onChange={(e) => setNewTool(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && addItem('current_data_tools', newTool, setNewTool)}
                className="flex-1"
              />
              <Button 
                type="button" 
                onClick={() => addItem('current_data_tools', newTool, setNewTool)} 
                variant="outline"
              >
                Add
              </Button>
            </div>
            {formData.data_landscape.current_data_tools.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {formData.data_landscape.current_data_tools.map((tool) => (
                  <Badge key={tool} variant="outline" className="flex items-center space-x-1">
                    <span>{tool}</span>
                    <X 
                      className="w-3 h-3 cursor-pointer hover:text-red-500" 
                      onClick={() => removeItem('current_data_tools', tool)}
                    />
                  </Badge>
                ))}
              </div>
            )}
          </div>

          {/* Data Governance Maturity */}
          <div className="space-y-2">
            <Label className="text-sm font-medium">Data Governance Maturity</Label>
            <Select 
              value={formData.data_landscape.data_governance_maturity} 
              onValueChange={(value) => updateFormData('data_landscape', { data_governance_maturity: value })}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select current maturity level" />
              </SelectTrigger>
              <SelectContent>
                {maturityLevels.map((level) => (
                  <SelectItem key={level} value={level}>
                    {maturityLabels[level]}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Data Quality Issues */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">Data Quality Issues</Label>
            <div className="flex space-x-2">
              <Input
                placeholder="Add quality issue (e.g., Duplicates, Missing values)"
                value={newQualityIssue}
                onChange={(e) => setNewQualityIssue(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && addItem('data_quality_issues', newQualityIssue, setNewQualityIssue)}
                className="flex-1"
              />
              <Button 
                type="button" 
                onClick={() => addItem('data_quality_issues', newQualityIssue, setNewQualityIssue)} 
                variant="outline"
              >
                Add
              </Button>
            </div>
            {formData.data_landscape.data_quality_issues.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {formData.data_landscape.data_quality_issues.map((issue) => (
                  <Badge key={issue} variant="destructive" className="flex items-center space-x-1">
                    <span>{issue}</span>
                    <X 
                      className="w-3 h-3 cursor-pointer hover:text-red-300" 
                      onClick={() => removeItem('data_quality_issues', issue)}
                    />
                  </Badge>
                ))}
              </div>
            )}
          </div>

          {/* Compliance Challenges */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">Compliance Challenges</Label>
            <div className="flex space-x-2">
              <Input
                placeholder="Add compliance challenge (e.g., Data retention, Access controls)"
                value={newComplianceChallenge}
                onChange={(e) => setNewComplianceChallenge(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && addItem('compliance_challenges', newComplianceChallenge, setNewComplianceChallenge)}
                className="flex-1"
              />
              <Button 
                type="button" 
                onClick={() => addItem('compliance_challenges', newComplianceChallenge, setNewComplianceChallenge)} 
                variant="outline"
              >
                Add
              </Button>
            </div>
            {formData.data_landscape.compliance_challenges.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {formData.data_landscape.compliance_challenges.map((challenge) => (
                  <Badge key={challenge} variant="destructive" className="flex items-center space-x-1">
                    <span>{challenge}</span>
                    <X 
                      className="w-3 h-3 cursor-pointer hover:text-red-300" 
                      onClick={() => removeItem('compliance_challenges', challenge)}
                    />
                  </Badge>
                ))}
              </div>
            )}
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

export default DataLandscapeStep

