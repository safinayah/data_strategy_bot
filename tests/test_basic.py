"""
Test Suite for Data Strategy Bot
Basic tests to verify functionality
"""

import unittest
import os
import sys
import json
from unittest.mock import Mock, patch

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.organization import OrganizationalInput, OrganizationalProfile, IndustryType, CompanySize, BusinessModel
from models.recommendations import DataStrategyRecommendation, RecommendationArea, PriorityLevel

class TestOrganizationalModels(unittest.TestCase):
    """Test organizational data models"""
    
    def setUp(self):
        """Set up test data"""
        self.sample_profile = OrganizationalProfile(
            company_name="Test Company",
            industry=IndustryType.TECHNOLOGY,
            company_size=CompanySize.MEDIUM,
            business_model=BusinessModel.B2B,
            geographic_presence=["US", "Canada"],
            regulatory_requirements=["GDPR", "SOX"]
        )
    
    def test_organizational_profile_creation(self):
        """Test creating organizational profile"""
        self.assertEqual(self.sample_profile.company_name, "Test Company")
        self.assertEqual(self.sample_profile.industry, IndustryType.TECHNOLOGY)
        self.assertIn("US", self.sample_profile.geographic_presence)
    
    def test_priority_areas_detection(self):
        """Test priority area detection logic"""
        # This would require a full OrganizationalInput object
        # Simplified test for now
        self.assertTrue(True)  # Placeholder

class TestRecommendationModels(unittest.TestCase):
    """Test recommendation data models"""
    
    def test_recommendation_area_creation(self):
        """Test creating recommendation area"""
        rec_area = RecommendationArea(
            title="Data Governance",
            priority=PriorityLevel.HIGH,
            weight=11,
            current_state_assessment="Initial maturity level",
            recommended_actions=["Establish governance council"],
            implementation_steps=["Step 1", "Step 2"],
            success_metrics=["Metric 1"],
            estimated_timeline="6 months",
            resource_requirements=["Data steward"],
            potential_challenges=["Change resistance"]
        )
        
        self.assertEqual(rec_area.title, "Data Governance")
        self.assertEqual(rec_area.priority, PriorityLevel.HIGH)
        self.assertEqual(rec_area.weight, 11)

class TestKnowledgeBase(unittest.TestCase):
    """Test knowledge base functionality"""
    
    @patch('utils.qdrant_client.QdrantClient')
    @patch('openai.OpenAI')
    def test_knowledge_base_initialization(self, mock_openai, mock_qdrant):
        """Test knowledge base initialization"""
        # Mock the clients to avoid actual API calls
        mock_qdrant_instance = Mock()
        mock_openai_instance = Mock()
        mock_qdrant.return_value = mock_qdrant_instance
        mock_openai.return_value = mock_openai_instance
        
        # This would test the actual initialization
        # For now, just verify mocks are set up
        self.assertTrue(True)  # Placeholder

if __name__ == '__main__':
    # Create test data directory
    os.makedirs('test_data', exist_ok=True)
    
    # Run tests
    unittest.main()

