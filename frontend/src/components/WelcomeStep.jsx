import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { 
  ChevronRight, 
  BarChart3, 
  Target, 
  Shield, 
  Zap,
  Users,
  TrendingUp
} from 'lucide-react'

const WelcomeStep = ({ nextStep }) => {
  const features = [
    {
      icon: BarChart3,
      title: 'DMBOK Framework',
      description: 'Based on industry-standard Data Management Body of Knowledge'
    },
    {
      icon: Target,
      title: 'Tailored Recommendations',
      description: 'Personalized strategies based on your organization\'s unique needs'
    },
    {
      icon: Shield,
      title: 'Compliance Ready',
      description: 'Addresses regulatory requirements and industry standards'
    },
    {
      icon: Zap,
      title: 'AI-Powered Insights',
      description: 'Advanced AI analysis for comprehensive strategy development'
    },
    {
      icon: Users,
      title: 'Executive Ready',
      description: 'Professional reports suitable for leadership presentations'
    },
    {
      icon: TrendingUp,
      title: 'ROI Focused',
      description: 'Clear business value and implementation roadmaps'
    }
  ]

  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <Card className="border-0 shadow-lg bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
          <CardHeader className="text-center pb-8">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
              className="w-16 h-16 bg-white bg-opacity-20 rounded-full flex items-center justify-center mx-auto mb-4"
            >
              <BarChart3 className="w-8 h-8" />
            </motion.div>
            <CardTitle className="text-3xl font-bold mb-2">
              Welcome to Data Strategy Bot
            </CardTitle>
            <CardDescription className="text-blue-100 text-lg max-w-2xl mx-auto">
              Generate comprehensive, AI-powered data strategy recommendations tailored to your organization's unique needs and challenges.
            </CardDescription>
          </CardHeader>
        </Card>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.6 }}
      >
        <Card>
          <CardHeader>
            <CardTitle className="text-xl">What You'll Get</CardTitle>
            <CardDescription>
              Our comprehensive assessment will provide you with:
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {features.map((feature, index) => {
                const Icon = feature.icon
                return (
                  <motion.div
                    key={feature.title}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.4 + index * 0.1, duration: 0.5 }}
                    className="flex items-start space-x-3 p-4 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors"
                  >
                    <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                      <Icon className="w-5 h-5 text-blue-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-1">{feature.title}</h3>
                      <p className="text-sm text-gray-600">{feature.description}</p>
                    </div>
                  </motion.div>
                )
              })}
            </div>
          </CardContent>
        </Card>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6, duration: 0.6 }}
      >
        <Card className="bg-gradient-to-r from-green-50 to-blue-50 border-green-200">
          <CardContent className="pt-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Ready to Transform Your Data Strategy?
              </h3>
              <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
                This assessment takes approximately 10-15 minutes to complete. 
                You'll answer questions about your organization, data landscape, and business objectives 
                to receive personalized recommendations.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                <div className="flex items-center space-x-2 text-sm text-gray-500">
                  <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                  <span>6 simple steps</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-500">
                  <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                  <span>AI-powered analysis</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-500">
                  <span className="w-2 h-2 bg-purple-500 rounded-full"></span>
                  <span>Executive-ready reports</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8, duration: 0.6 }}
        className="flex justify-center"
      >
        <Button 
          onClick={nextStep}
          size="lg"
          className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200"
        >
          Start Assessment
          <ChevronRight className="ml-2 w-5 h-5" />
        </Button>
      </motion.div>
    </div>
  )
}

export default WelcomeStep

