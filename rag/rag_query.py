#!/usr/bin/env python3
"""
Minimal RAG pipeline for querying the OKF Home-Lab Infrastructure bundle
"""

import os
import re
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from pathlib import Path
from typing import List, Dict, Tuple, Optional

class OKFRAGPipeline:
    def __init__(self, bundle_path: str):
        """
        Initialize the RAG pipeline
        
        Args:
            bundle_path: Path to the OKF bundle root directory
        """
        self.bundle_path = Path(bundle_path)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents = []  # List of (content, metadata) tuples
        self.index = None
        self._load_documents()
        self._build_index()
    
    def _extract_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """
        Extract YAML frontmatter from markdown content
        
        Returns:
            Tuple of (frontmatter_dict, body_content)
        """
        frontmatter = {}
        body = content
        
        # Check for frontmatter delimiter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    body = parts[2]
                except:
                    pass  # If parsing fails, treat as no frontmatter
        
        return frontmatter, body
    
    def _load_documents(self):
        """Load all markdown documents from the bundle"""
        import yaml  # Import here to avoid issues if not installed
        
        # Find all .md files
        md_files = list(self.bundle_path.rglob("*.md"))
        
        for md_file in md_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract frontmatter and body
                frontmatter, body = self._extract_frontmatter(content)
                
                # Clean up body text
                body = re.sub(r'\s+', ' ', body).strip()
                
                if body:  # Only add if there's content
                    # Create metadata
                    metadata = {
                        'path': str(md_file.relative_to(self.bundle_path)),
                        'title': frontmatter.get('title', 'Untitled'),
                        'type': frontmatter.get('type', 'Unknown'),
                        'tags': frontmatter.get('tags', []),
                        'sources': frontmatter.get('sources', [])
                    }
                    
                    self.documents.append((body, metadata))
                    
            except Exception as e:
                print(f"Warning: Could not process {md_file}: {e}")
    
    def _build_index(self):
        """Build FAISS index from document embeddings"""
        if not self.documents:
            print("No documents loaded")
            return
        
        # Extract text content for embedding
        texts = [doc[0] for doc in self.documents]
        
        # Generate embeddings
        print(f"Generating embeddings for {len(texts)} documents...")
        embeddings = self.model.encode(texts)
        
        # Build FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))
        
        print(f"Built index with {self.index.ntotal} vectors")
    
    def query(self, question: str, k: int = 3) -> List[Dict]:
        """
        Query the knowledge base
        
        Args:
            question: The question to ask
            k: Number of results to return
            
        Returns:
            List of relevant documents with metadata
        """
        if self.index is None:
            return [{"error": "Index not built"}]
        
        # Encode the question
        question_embedding = self.model.encode([question])
        
        # Search the index
        distances, indices = self.index.search(
            question_embedding.astype('float32'), k
        )
        
        # Prepare results
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.documents):
                content, metadata = self.documents[idx]
                results.append({
                    'rank': i + 1,
                    'content': content[:500] + "..." if len(content) > 500 else content,
                    'metadata': metadata,
                    'distance': float(distance),
                    'relevance_score': 1.0 / (1.0 + float(distance))  # Convert distance to similarity
                })
        
        return results
    
    def query_with_answer(self, question: str, k: int = 3) -> Dict:
        """
        Query and generate a grounded answer (simplified version)
        
        Args:
            question: The question to ask
            k: Number of context documents to use
            
        Returns:
            Dictionary with answer and sources
        """
        # Get relevant documents
        results = self.query(question, k)
        
        if not results or 'error' in results[0]:
            return {
                'answer': "Unable to retrieve relevant information",
                'sources': [],
                'confidence': 0.0
            }
        
        # Extract context from top results
        context_parts = []
        sources = []
        
        for result in results:
            context_parts.append(result['content'])
            sources.append({
                'title': result['metadata']['title'],
                'type': result['metadata']['type'],
                'path': result['metadata']['path'],
                'relevance': result['relevance_score']
            })
        
        context = "\n\n---\n\n".join(context_parts)
        
        # Simple answer generation (in a real implementation, this would use an LLM)
        # For now, we'll return the most relevant content as the answer
        best_result = results[0]
        
        return {
            'answer': f"Based on the documentation:\n\n{best_result['content']}",
            'sources': sources,
            'confidence': best_result['relevance_score'],
            'query': question
        }

def main():
    """Example usage of the RAG pipeline"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Query the OKF Home-Lab bundle')
    parser.add_argument('question', nargs='?', default="What is the Jellyfin health-check command?",
                       help='Question to ask about the home-lab infrastructure')
    parser.add_argument('--bundle', default='.',
                       help='Path to the OKF bundle root directory')
    parser.add_argument('--k', type=int, default=3,
                       help='Number of results to return')
    
    args = parser.parse_args()
    
    # Initialize pipeline
    print(f"Loading OKF bundle from {args.bundle}...")
    pipeline = OKFRAGPipeline(args.bundle)
    
    # Query
    print(f"\nQuery: {args.question}")
    print("-" * 50)
    
    result = pipeline.query_with_answer(args.question, args.k)
    
    print(f"Answer:\n{result['answer']}")
    print(f"\nConfidence: {result['confidence']:.2f}")
    print(f"\nSources:")
    for i, source in enumerate(result['sources'], 1):
        print(f"  {i}. {source['title']} ({source['type']})")
        print(f"     Path: {source['path']}")
        print(f"     Relevance: {source['relevance']:.2f}")

if __name__ == "__main__":
    main()