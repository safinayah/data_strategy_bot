"""
Knowledge Base Manager
Handles initialization and management of DMBOK knowledge in vector database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.dmbok_knowledge.knowledge_base import DMBOK_KNOWLEDGE_AREAS
from utils.qdrant_client import QdrantVectorStore

class KnowledgeBaseManager:
    def __init__(self):
        self.vector_store = QdrantVectorStore()
        
    def initialize_knowledge_base(self):
        """Initialize the vector database with DMBOK knowledge"""
        print("Initializing DMBOK knowledge base...")
        
        # Create collection
        self.vector_store.create_collection()
        
        # Add each knowledge area
        success_count = 0
        for area_id, knowledge_area in DMBOK_KNOWLEDGE_AREAS.items():
            if self.vector_store.add_knowledge_area(knowledge_area, area_id):
                success_count += 1
        
        print(f"Successfully added {success_count}/{len(DMBOK_KNOWLEDGE_AREAS)} knowledge areas")
        return success_count == len(DMBOK_KNOWLEDGE_AREAS)
    
    def search_relevant_knowledge(self, organizational_context: str, limit: int = 5):
        """Search for knowledge relevant to organizational context"""
        return self.vector_store.search_knowledge(organizational_context, limit)
    
    def get_knowledge_by_priority(self, priorities: list):
        """Get knowledge areas by priority (based on CDMP weights)"""
        all_areas = self.vector_store.get_all_knowledge_areas()
        
        # Sort by weight (higher weight = higher priority)
        sorted_areas = sorted(all_areas, key=lambda x: x.get('weight', 0), reverse=True)
        
        # Filter by priorities if specified
        if priorities:
            priority_titles = [area.lower().replace('_', ' ') for area in priorities]
            filtered_areas = [
                area for area in sorted_areas 
                if area['title'].lower() in priority_titles
            ]
            return filtered_areas
        
        return sorted_areas
    
    def test_knowledge_retrieval(self):
        """Test knowledge retrieval functionality"""
        print("Testing knowledge retrieval...")
        
        test_queries = [
            "data governance framework for startup",
            "data quality management best practices",
            "data architecture for cloud migration",
            "metadata management implementation"
        ]
        
        for query in test_queries:
            print(f"\nQuery: {query}")
            results = self.search_relevant_knowledge(query, limit=3)
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result['title']} (Score: {result['score']:.3f})")

if __name__ == "__main__":
    # Initialize knowledge base
    kb_manager = KnowledgeBaseManager()
    
    # Check if we should initialize
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        kb_manager.initialize_knowledge_base()
    elif len(sys.argv) > 1 and sys.argv[1] == "test":
        kb_manager.test_knowledge_retrieval()
    else:
        print("Usage:")
        print("  python knowledge_base_manager.py init  - Initialize knowledge base")
        print("  python knowledge_base_manager.py test  - Test knowledge retrieval")

