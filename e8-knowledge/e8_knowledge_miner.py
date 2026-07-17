#!/usr/bin/env python3
"""
E8 KNOWLEDGE MINER
Extract and index mathematical knowledge from PDF collection

Purpose: Mine the 'true kinowlege' folder for E8, Lie groups,
         gauge theory, and exceptional mathematical structures.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict

# Configuration
KNOWLEDGE_DIR = Path("/sdcard/hermes brain plug/the true kinowlege")
INDEX_FILE = Path.home() / ".e8_knowledge_index.json"

@dataclass
class MathematicalConcept:
    """A mathematical concept extracted from literature."""
    name: str
    category: str  # E8, LieGroup, GaugeTheory, etc.
    source_files: List[str]
    related_concepts: List[str]
    description: str
    extracted_date: str

@dataclass
class PDFDocument:
    """Metadata about a PDF document."""
    filename: str
    arxiv_id: Optional[str]
    title: Optional[str]
    authors: List[str]
    year: Optional[int]
    size_mb: float
    concepts_found: List[str]

class E8KnowledgeMiner:
    """Mine E8 and exceptional mathematics from PDF collection."""
    
    # Mathematical terms to search for
    CONCEPT_PATTERNS = {
        "E8": [r'\bE8\b', r'\bE_8\b', r'exceptional.*lie', r'lie.*exceptional'],
        "LieGroup": [r'\bLie group', r'\bLie algebra', r'semisimple', r'compact lie'],
        "GaugeTheory": [r'gauge theory', r'BRST', r'Yang-Mills', r'fiber bundle'],
        "Supersymmetry": [r'supersymmetry', r'supergravity', r'superstring', r'supercharge'],
        "CliffordAlgebra": [r'Clifford algebra', r'geometric algebra', r'spinor'],
        "Cohomology": [r'cohomology', r'BRST cohomology', r'Chevalley', r'Weil'],
        "RootSystem": [r'root system', r'Weyl group', r'Cartan', r'Dynkin diagram'],
        "StringTheory": [r'string theory', r'M-theory', r'brane', r'compactification'],
        "GrandUnification": [r'grand unified', r'GUT', r'standard model', r'fermion'],
    }
    
    def __init__(self):
        self.documents: List[PDFDocument] = []
        self.concepts: Dict[str, MathematicalConcept] = {}
        self.knowledge_graph: Dict[str, List[str]] = {}
    
    def scan_collection(self) -> List[PDFDocument]:
        """Scan the PDF collection and extract metadata."""
        print(f"[*] Scanning {KNOWLEDGE_DIR}...")
        
        pdf_files = sorted(KNOWLEDGE_DIR.glob("*.pdf"))
        print(f"[*] Found {len(pdf_files)} PDF documents")
        
        for pdf_path in pdf_files:
            doc = self._analyze_pdf(pdf_path)
            self.documents.append(doc)
        
        return self.documents
    
    def _analyze_pdf(self, pdf_path: Path) -> PDFDocument:
        """Analyze a single PDF file."""
        filename = pdf_path.name
        size_mb = pdf_path.stat().st_size / (1024 * 1024)
        
        # Try to extract arXiv ID from filename
        arxiv_match = re.match(r'(\d{4,7}\.?\d{0,4})', filename)
        arxiv_id = arxiv_match.group(1) if arxiv_match else None
        
        # Try to extract year from filename
        year_match = re.match(r'(\d{2})\d{4}', filename)
        year = None
        if year_match:
            year_prefix = int(year_match.group(1))
            year = 1900 + year_prefix if year_prefix >= 90 else 2000 + year_prefix
        
        # Analyze title from filename
        title = self._extract_title_from_filename(filename)
        
        # Search for mathematical concepts in filename
        concepts_found = []
        filename_lower = filename.lower()
        for concept, patterns in self.CONCEPT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, filename_lower):
                    concepts_found.append(concept)
                    break
        
        return PDFDocument(
            filename=filename,
            arxiv_id=arxiv_id,
            title=title,
            authors=[],  # Would need PDF text extraction
            year=year,
            size_mb=round(size_mb, 2),
            concepts_found=list(set(concepts_found))
        )
    
    def _extract_title_from_filename(self, filename: str) -> Optional[str]:
        """Try to extract a readable title from PDF filename."""
        # Remove .pdf and arxiv numbers
        title = re.sub(r'\.pdf$', '', filename)
        title = re.sub(r'^\d+[a-z]?\.?', '', title)
        title = re.sub(r'^v\d+', '', title)
        
        # Convert underscores and hyphens to spaces
        title = title.replace('_', ' ').replace('-', ' ')
        
        # Capitalize words
        title = ' '.join(word.capitalize() for word in title.split())
        
        return title if title else None
    
    def build_knowledge_index(self) -> Dict:
        """Build a searchable index of mathematical knowledge."""
        print("[*] Building knowledge index...")
        
        index = {
            "total_documents": len(self.documents),
            "total_size_mb": round(sum(d.size_mb for d in self.documents), 2),
            "categories": {},
            "by_year": {},
            "concepts": {},
            "documents": []
        }
        
        # Categorize by concepts found
        for doc in self.documents:
            # Add to year index
            if doc.year:
                year_str = str(doc.year)
                if year_str not in index["by_year"]:
                    index["by_year"][year_str] = []
                index["by_year"][year_str].append(doc.filename)
            
            # Add to concept index
            for concept in doc.concepts_found:
                if concept not in index["concepts"]:
                    index["concepts"][concept] = {
                        "count": 0,
                        "documents": []
                    }
                index["concepts"][concept]["count"] += 1
                index["concepts"][concept]["documents"].append(doc.filename)
        
        # Add document summaries
        for doc in self.documents:
            index["documents"].append({
                "filename": doc.filename,
                "title": doc.title,
                "arxiv_id": doc.arxiv_id,
                "year": doc.year,
                "size_mb": doc.size_mb,
                "concepts": doc.concepts_found
            })
        
        return index
    
    def find_e8_papers(self) -> List[PDFDocument]:
        """Find all papers related to E8."""
        e8_papers = []
        for doc in self.documents:
            if "E8" in doc.concepts_found or \
               any(re.search(r'E[_-]?8', doc.filename, re.I) for doc in [doc]):
                e8_papers.append(doc)
        return e8_papers
    
    def find_lie_group_papers(self) -> List[PDFDocument]:
        """Find all papers related to Lie groups."""
        lie_papers = []
        for doc in self.documents:
            if any(c in doc.concepts_found for c in ["LieGroup", "E8", "RootSystem"]):
                lie_papers.append(doc)
        return lie_papers
    
    def save_index(self, index: Dict):
        """Save the knowledge index to disk."""
        with open(INDEX_FILE, 'w') as f:
            json.dump(index, f, indent=2)
        print(f"[*] Index saved to {INDEX_FILE}")
    
    def print_summary(self):
        """Print a summary of the collection."""
        print("\n" + "="*60)
        print("E8 KNOWLEDGE COLLECTION SUMMARY")
        print("="*60)
        print(f"Total Documents: {len(self.documents)}")
        print(f"Total Size: {sum(d.size_mb for d in self.documents):.2f} MB")
        print()
        
        # Count by concept
        concept_counts = {}
        for doc in self.documents:
            for concept in doc.concepts_found:
                concept_counts[concept] = concept_counts.get(concept, 0) + 1
        
        if concept_counts:
            print("Mathematical Concepts Found:")
            for concept, count in sorted(concept_counts.items(), key=lambda x: -x[1]):
                print(f"  {concept:<20} {count:>3} documents")
        
        # Year distribution
        years = [d.year for d in self.documents if d.year]
        if years:
            print(f"\nYear Range: {min(years)} - {max(years)}")
        
        # Largest files
        print("\nLargest Documents:")
        for doc in sorted(self.documents, key=lambda x: -x.size_mb)[:5]:
            print(f"  {doc.filename:<35} {doc.size_mb:>6.2f} MB")
        
        print()


def main():
    """Main entry point."""
    miner = E8KnowledgeMiner()
    
    # Scan the collection
    miner.scan_collection()
    
    # Print summary
    miner.print_summary()
    
    # Build and save index
    index = miner.build_knowledge_index()
    miner.save_index(index)
    
    # Find specific papers
    e8_papers = miner.find_e8_papers()
    lie_papers = miner.find_lie_group_papers()
    
    print(f"E8-related papers: {len(e8_papers)}")
    print(f"Lie group papers: {len(lie_papers)}")
    
    # Interactive search
    print("\n" + "="*60)
    print("Available Commands:")
    print("  search <concept>  - Search for papers by concept")
    print("  list             - List all documents")
    print("  e8               - List E8-specific papers")
    print("  quit             - Exit")
    print("="*60)
    
    while True:
        try:
            cmd = input("\n> ").strip().lower()
            
            if cmd == 'quit':
                break
            elif cmd == 'list':
                for doc in sorted(miner.documents, key=lambda x: x.filename):
                    concepts = ', '.join(doc.concepts_found) if doc.concepts_found else 'N/A'
                    print(f"  {doc.filename:<40} {concepts}")
            elif cmd == 'e8':
                print("\nE8-related Papers:")
                for doc in e8_papers:
                    print(f"  - {doc.filename}")
                    if doc.title:
                        print(f"    Title: {doc.title}")
            elif cmd.startswith('search '):
                term = cmd[7:].strip()
                matches = [d for d in miner.documents 
                          if term.lower() in d.filename.lower() 
                          or any(term.lower() in c.lower() for c in d.concepts_found)]
                print(f"\nFound {len(matches)} matches for '{term}':")
                for doc in matches[:10]:
                    print(f"  - {doc.filename}")
            else:
                print("Unknown command. Type 'list', 'e8', 'search <term>', or 'quit'")
        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()
