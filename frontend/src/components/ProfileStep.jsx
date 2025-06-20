import { useState } from 'react'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { ChevronRight, ChevronLeft, Building2, X } from 'lucide-react'

const ProfileStep = ({ formData, updateFormData, nextStep, prevStep }) => {
  const [newLocation, setNewLocation] = useState('')
  const [newRequirement, setNewRequirement] = useState('')

  const industries = [
    'Healthcare', 'Financial Services', 'Technology', 'Manufacturing', 
    'Retail', 'Education', 'Government', 'Energy', 'Transportation', 
    'Media & Entertainment', 'Real Estate', 'Other'
  ]

  const companySizes = [
    'Startup (1-10 employees)',
    'Small (11-50 employees)', 
    'Medium (51-250 employees)',
    'Large (251-1000 employees)',
    'Enterprise (1000+ employees)'
  ]

  const businessModels = [
    'B2B (Business to Business)',
    'B2C (Business to Consumer)',
    'B2B2C (Business to Business to Consumer)',
    'Marketplace',
    'SaaS (Software as a Service)',
    'Non-profit',
    'Government',
    'Other'
  ]

  const addLocation = () => {
    if (newLocation.trim() && !formData.profile.geographic_presence.includes(newLocation.trim())) {
      updateFormData('profile', {
        geographic_presence: [...formData.profile.geographic_presence, newLocation.trim()]
      })
      setNewLocation('')
    }
  }

  const removeLocation = (location) => {
    updateFormData('profile', {
      geographic_presence: formData.profile.geographic_presence.filter(l => l !== location)
    })
  }

  const addRequirement = () => {
    if (newRequirement.trim() && !formData.profile.regulatory_requirements.includes(newRequirement.trim())) {
      updateFormData('profile', {
        regulatory_requirements: [...formData.profile.regulatory_requirements, newRequirement.trim()]
      })
      setNewRequirement('')
    }
  }

  const removeRequirement = (requirement) => {
    updateFormData('profile', {
      regulatory_requirements: formData.profile.regulatory_requirements.filter(r => r !== requirement)
    })
  }

  const isValid = formData.profile.company_name && formData.profile.industry && formData.profile.company_size

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
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <Building2 className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <CardTitle className="text-xl">Organization Profile</CardTitle>
              <CardDescription>
                Tell us about your organization to personalize your recommendations
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Company Name */}
          <div className="space-y-2">
            <Label htmlFor="company_name" className="text-sm font-medium">
              Company Name *
            </Label>
            <Input
              id="company_name"
              placeholder="Enter your company name"
              value={formData.profile.company_name}
              onChange={(e) => updateFormData('profile', { company_name: e.target.value })}
              className="w-full"
            />
          </div>

          {/* Industry */}
          <div className="space-y-2">
            <Label className="text-sm font-medium">Industry *</Label>
            <Select 
              value={formData.profile.industry} 
              onValueChange={(value) => updateFormData('profile', { industry: value })}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select your industry" />
              </SelectTrigger>
              <SelectContent>
                {industries.map((industry) => (
                  <SelectItem key={industry} value={industry.toLowerCase()}>
                    {industry}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Company Size */}
          <div className="space-y-2">
            <Label className="text-sm font-medium">Company Size *</Label>
            <Select 
              value={formData.profile.company_size} 
              onValueChange={(value) => updateFormData('profile', { company_size: value })}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select company size" />
              </SelectTrigger>
              <SelectContent>
                {companySizes.map((size) => (
                  <SelectItem key={size} value={size.toLowerCase()}>
                    {size}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Business Model */}
          <div className="space-y-2">
            <Label className="text-sm font-medium">Business Model</Label>
            <Select 
              value={formData.profile.business_model} 
              onValueChange={(value) => updateFormData('profile', { business_model: value })}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select business model (optional)" />
              </SelectTrigger>
              <SelectContent>
                {businessModels.map((model) => (
                  <SelectItem key={model} value={model.toLowerCase()}>
                    {model}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Geographic Presence */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">Geographic Presence</Label>
            <div className="flex space-x-2">
              <Input
                placeholder="Add location (e.g., North America, Europe)"
                value={newLocation}
                onChange={(e) => setNewLocation(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && addLocation()}
                className="flex-1"
              />
              <Button type="button" onClick={addLocation} variant="outline">
                Add
              </Button>
            </div>
            {formData.profile.geographic_presence.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {formData.profile.geographic_presence.map((location) => (
                  <Badge key={location} variant="secondary" className="flex items-center space-x-1">
                    <span>{location}</span>
                    <X 
                      className="w-3 h-3 cursor-pointer hover:text-red-500" 
                      onClick={() => removeLocation(location)}
                    />
                  </Badge>
                ))}
              </div>
            )}
          </div>

          {/* Regulatory Requirements */}
          <div className="space-y-3">
            <Label className="text-sm font-medium">Regulatory Requirements</Label>
            <div className="flex space-x-2">
              <Input
                placeholder="Add requirement (e.g., GDPR, HIPAA, SOX)"
                value={newRequirement}
                onChange={(e) => setNewRequirement(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && addRequirement()}
                className="flex-1"
              />
              <Button type="button" onClick={addRequirement} variant="outline">
                Add
              </Button>
            </div>
            {formData.profile.regulatory_requirements.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {formData.profile.regulatory_requirements.map((requirement) => (
                  <Badge key={requirement} variant="secondary" className="flex items-center space-x-1">
                    <span>{requirement}</span>
                    <X 
                      className="w-3 h-3 cursor-pointer hover:text-red-500" 
                      onClick={() => removeRequirement(requirement)}
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

export default ProfileStep

