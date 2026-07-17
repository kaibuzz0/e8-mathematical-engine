#!/usr/bin/env python3
"""
HERMES BRAIN PLUG LIBRARY INDEXER v1.0
Massive knowledge base indexing system

Scans and catalogs 577+ books (4.49 GB) from:
/sdcard/hermes brain plug/books/

Categories discovered:
- Financial economics, econometrics
- Physics (Dirac sea, quantum theory)
- Self-help and psychology
- Food preservation and homesteading
- Communication and leadership
- Free energy patents
- Walter Russell (fulcrum science)
- And hundreds more...

This is a survival/prepper knowledge vault + advanced physics library
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict

BOOKS_DIR = Path("/sdcard/hermes brain plug/books")
INDEX_FILE = Path.home() / ".hermes_library_index.json"

@dataclass
class BookEntry:
    """A book in the Hermès library."""
    filename: str
    title: str
    category: str
    size_mb: float
    topics: List[str]
    
@dataclass
class CategoryStats:
    """Statistics for a book category."""
    name: str
    count: int
    total_size_mb: float
    sample_titles: List[str]

class HermesLibraryIndexer:
    """Index the massive Hermès brain plug library."""
    
    # Topic patterns for categorization
    CATEGORY_PATTERNS = {
        "Physics": [
            r'physics', r'quantum', r'dirac', r'electrodynamic', r'field',
            r'relativity', r'thermodynamic', r'mechanic', r'energy',
            r'walter.russell', r'fulcrum', r'vacuum', r'plasma'
        ],
        "Mathematics": [
            r'mathematic', r'geometry', r'algebra', r'calculus',
            r'topology', r'number.theory', r'statistic'
        ],
        "Financial": [
            r'financ', r'econometric', r'econom', r'invest',
            r'monetar', r'exchange', r'bank', r'market',
            r'stock', r'portfolio', r'money'
        ],
        "Self_Help": [
            r'stress', r'finding.yourself', r'solo', r'under.30',
            r'communicat', r'leadership', r'psychology',
            r'personal', r'development'
        ],
        "Survival": [
            r'canning', r'preserv', r'freeze', r'food',
            r'fisheries', r'aquaculture', r'jars', r'jell',
            r'prepping', r'homestead'
        ],
        "Technology": [
            r'patent', r'free.energy', r'flynn', r'flywheel',
            r'electronic', r'computer', r'software',
            r'frontpage', r'ocr'
        ],
        "Spiritual": [
            r'phallic', r'faith', r'deit', r'spirit',
            r'religion', r'sacred', r'flower', r'element'
        ],
        "History": [
            r'histor', r'photograph', r'document', r'japanese',
            r'war', r'archive'
        ],
        "Business": [
            r'business', r'institution', r'corporate',
            r'pr', r'public.relation', r'friction'
        ]
    }
    
    def __init__(self):
        self.books: List[BookEntry] = []
        self.categories: Dict[str, CategoryStats] = {}
        self.total_books = 0
        self.total_size_gb = 0.0
    
    def scan_library(self) -> List[BookEntry]:
        """Scan the books directory."""
        print(f"[*] Scanning {BOOKS_DIR}...")
        
        pdf_files = sorted(BOOKS_DIR.glob("*.pdf"))
        print(f"[*] Found {len(pdf_files)} books")
        
        for pdf_path in pdf_files:
            book = self._analyze_book(pdf_path)
            self.books.append(book)
        
        self.total_books = len(self.books)
        self.total_size_gb = sum(b.size_mb for b in self.books) / 1024
        
        return self.books
    
    def _analyze_book(self, pdf_path: Path) -> BookEntry:
        """Analyze a single book."""
        filename = pdf_path.name
        size_mb = pdf_path.stat().st_size / (1024 * 1024)
        
        # Extract title from filename
        title = self._clean_filename(filename)
        
        # Categorize
        category, topics = self._categorize(filename)
        
        return BookEntry(
            filename=filename,
            title=title,
            category=category,
            size_mb=round(size_mb, 2),
            topics=topics
        )
    
    def _clean_filename(self, filename: str) -> str:
        """Clean filename to extract title."""
        # Remove .pdf
        title = filename.replace('.pdf', '')
        
        # Replace underscores and hyphens with spaces
        title = title.replace('_', ' ').replace('-', ' ')
        
        # Remove extra spaces
        title = ' '.join(title.split())
        
        return title
    
    def _categorize(self, filename: str) -> Tuple[str, List[str]]:
        """Categorize a book based on filename."""
        filename_lower = filename.lower()
        matched_topics = []
        
        for category, patterns in self.CATEGORY_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, filename_lower):
                    matched_topics.append(category)
                    break
        
        # Return primary category or "Uncategorized"
        primary = matched_topics[0] if matched_topics else "Uncategorized"
        return primary, matched_topics
    
    def build_category_stats(self) -> Dict[str, CategoryStats]:
        """Build statistics for each category."""
        cat_data = defaultdict(lambda: {"count": 0, "size": 0.0, "titles": []})
        
        for book in self.books:
            cat = book.category
            cat_data[cat]["count"] += 1
            cat_data[cat]["size"] += book.size_mb
            cat_data[cat]["titles"].append(book.title[:60])
        
        self.categories = {}
        for cat, data in cat_data.items():
            self.categories[cat] = CategoryStats(
                name=cat,
                count=data["count"],
                total_size_mb=round(data["size"], 2),
                sample_titles=data["titles"][:5]
            )
        
        return self.categories
    
    def print_summary(self):
        """Print library summary."""
        print("\n" + "="*70)
        print("HERMES BRAIN PLUG LIBRARY INDEX")
        print("="*70)
        print(f"Total Books: {self.total_books}")
        print(f"Total Size: {self.total_size_gb:.2f} GB")
        print(f"Location: {BOOKS_DIR}")
        print()
        
        print("Category Breakdown:")
        print("-" * 70)
        
        # Sort by count
        sorted_cats = sorted(
            self.categories.items(),
            key=lambda x: x[1].count,
            reverse=True
        )
        
        for cat_name, stats in sorted_cats:
            print(f"\n{cat_name} ({stats.count} books, {stats.total_size_mb:.1f} MB)")
            for title in stats.sample_titles[:3]:
                print(f"  • {title}")
        
        print()
    
    def search_books(self, query: str) -> List[BookEntry]:
        """Search for books by keyword."""
        query_lower = query.lower()
        matches = []
        
        for book in self.books:
            if query_lower in book.title.lower() or \
               query_lower in book.category.lower() or \
               any(query_lower in t.lower() for t in book.topics):
                matches.append(book)
        
        return matches
    
    def export_index(self):
        """Export the library index to JSON."""
        index = {
            "metadata": {
                "total_books": self.total_books,
                "total_size_gb": round(self.total_size_gb, 2),
                "location": str(BOOKS_DIR),
                "date_indexed": str(Path.home() / ".hermes_library_index.json")
            },
            "categories": {},
            "books": []
        }
        
        # Add categories
        for cat_name, stats in self.categories.items():
            index["categories"][cat_name] = {
                "count": stats.count,
                "total_size_mb": stats.total_size_mb,
                "sample_titles": stats.sample_titles
            }
        
        # Add all books
        for book in self.books:
            index["books"].append({
                "filename": book.filename,
                "title": book.title,
                "category": book.category,
                "size_mb": book.size_mb,
                "topics": book.topics
            })
        
        with open(INDEX_FILE, 'w') as f:
            json.dump(index, f, indent=2)
        
        print(f"[*] Index exported to {INDEX_FILE}")
        
        return index


def main():
    """Main entry point."""
    indexer = HermesLibraryIndexer()
    
    # Scan the library
    indexer.scan_library()
    
    # Build category stats
    indexer.build_category_stats()
    
    # Print summary
    indexer.print_summary()
    
    # Export index
    indexer.export_index()
    
    print("="*70)
    print("Library indexing complete!")
    print("Commands: search <query>, list <category>, stats, quit")
    print("="*70)
    
    # Interactive mode
    while True:
        try:
            cmd = input("\n> ").strip().lower()
            
            if cmd == 'quit':
                break
            elif cmd == 'stats':
                indexer.print_summary()
            elif cmd.startswith('search '):
                query = cmd[7:]
                matches = indexer.search_books(query)
                print(f"\nFound {len(matches)} matches for '{query}':")
                for book in matches[:10]:
                    print(f"  • {book.title[:60]} ({book.category})")
            elif cmd.startswith('list '):
                cat = cmd[5:]
                if cat in indexer.categories:
                    stats = indexer.categories[cat]
                    print(f"\n{cat} ({stats.count} books):")
                    for title in stats.sample_titles:
                        print(f"  • {title}")
                else:
                    print(f"Category not found: {cat}")
            else:
                print("Commands: search <query>, list <category>, stats, quit")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()
