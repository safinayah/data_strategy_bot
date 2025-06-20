"""
Qdrant Vector Database Client
Handles vector storage and retrieval for DMBOK knowledge
"""

import os
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import openai
import numpy as np
from dotenv import load_dotenv
import uuid
load_dotenv()

class QdrantVectorStore:
    def __init__(self):
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        self.collection_name = "dmbok_knowledge"
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def create_collection(self, vector_size: int = 1536):
        """Create collection for DMBOK knowledge vectors"""
        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
            print(f"Collection '{self.collection_name}' created successfully")
        except Exception as e:
            print(f"Collection might already exist: {e}")
    
    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding using OpenAI"""
        try:
            response = self.openai_client.embeddings.create(
                input=text,
                model="text-embedding-ada-002"
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []
    
    def add_knowledge_area(self, knowledge_area: Dict[str, Any], area_id: str):
        """Add a knowledge area to the vector store"""
        # Create comprehensive text for embedding
        text_content = f"""
        Title: {knowledge_area['title']}
        Description: {knowledge_area['description']}
        Key Concepts: {', '.join(knowledge_area['key_concepts'])}
        Best Practices: {'. '.join(knowledge_area['best_practices'])}
        Implementation Steps: {'. '.join(knowledge_area['implementation_steps'])}
        Common Challenges: {', '.join(knowledge_area['common_challenges'])}
        Success Metrics: {', '.join(knowledge_area['success_metrics'])}
        """
        
        # Generate embedding
        embedding = self.get_embedding(text_content)
        if not embedding:
            return False
        
        # Create point for Qdrant
        point_id = str(uuid.uuid4())

        point = PointStruct(
            id=point_id,  # Use UUID instead of string
            vector=embedding,
            payload={
                "area_id": area_id,  # Store original area_id as metadata
                "title": knowledge_area["title"],
                "description": knowledge_area["description"],
                "weight": knowledge_area["weight"],
                "key_concepts": knowledge_area["key_concepts"],
                "best_practices": knowledge_area["best_practices"],
                "implementation_steps": knowledge_area["implementation_steps"],
                "common_challenges": knowledge_area["common_challenges"],
                "success_metrics": knowledge_area["success_metrics"],
                "content": text_content
            }
        )
        
        # Upload to Qdrant
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            print(f"Added knowledge area: {knowledge_area['title']}")
            return True
        except Exception as e:
            print(f"Error adding knowledge area: {e}")
            return False
    
    def search_knowledge(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant knowledge based on query"""
        # Generate query embedding
        query_embedding = self.get_embedding(query)
        if not query_embedding:
            return []
        
        try:
            # Search in Qdrant
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit
            )
            
            # Format results
            results = []
            for hit in search_result:
                results.append({
                    "score": hit.score,
                    "area_id":hit.payload.get("area_id",""),
                    "title": hit.payload["title"],
                    "description": hit.payload["description"],
                    "weight": hit.payload["weight"],
                    "key_concepts": hit.payload["key_concepts"],
                    "best_practices": hit.payload["best_practices"],
                    "implementation_steps": hit.payload["implementation_steps"],
                    "common_challenges": hit.payload["common_challenges"],
                    "success_metrics": hit.payload["success_metrics"]
                })
            
            return results
        except Exception as e:
            print(f"Error searching knowledge: {e}")
            return []
    
    def get_all_knowledge_areas(self) -> List[Dict[str, Any]]:
        """Retrieve all knowledge areas"""
        try:
            # Scroll through all points
            points, _ = self.client.scroll(
                collection_name=self.collection_name,
                limit=100
            )
            
            results = []
            for point in points:
                results.append({
                    "title": point.payload["title"],
                    "description": point.payload["description"],
                    "weight": point.payload["weight"],
                    "key_concepts": point.payload["key_concepts"],
                    "best_practices": point.payload["best_practices"],
                    "implementation_steps": point.payload["implementation_steps"],
                    "common_challenges": point.payload["common_challenges"],
                    "success_metrics": point.payload["success_metrics"]
                })
            
            return results
        except Exception as e:
            print(f"Error retrieving knowledge areas: {e}")
            return []

