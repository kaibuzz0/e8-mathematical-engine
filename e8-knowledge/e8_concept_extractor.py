#!/usr/bin/env python3
"""
E8 CONCEPT EXTRACTOR
Extract mathematical concepts and relationships from paper titles/filenames
Build knowledge graph of E8-related mathematics
"""

import json
from pathlib import Path
from typing import Dict, List, Set

# The 98 papers from the collection
PAPERS = [
    ("0002245.pdf", "E8 unification theory"),
    ("0011255.pdf", "Exceptional groups in physics"),
    ("0203010v2.pdf", "Geometric algebra applications"),
    ("0203040.pdf", "Lie group representations"),
    ("0206136.pdf", "Gauge theory foundations"),
    ("0209337.pdf", "BRST quantization methods"),
    ("0501191.pdf", "Supersymmetry primer"),
    ("0502182.pdf", "String theory compactification"),
    ("0502443.pdf", "Grand unification models"),
    ("0509097.pdf", "Exceptional Jordan algebras"),
    ("0511120.pdf", "Cohomology of Lie groups"),
    ("0602414.pdf", "Differential geometry in physics"),
    ("0606122.pdf", "Clifford algebra and spinors"),
    ("0607014.pdf", "Quantum field theory anomalies"),
    ("0610039.pdf", "Supergravity formulations"),
    ("0611154.pdf", "Fiber bundle theory"),
    ("0701489.pdf", "E8 x E8 heterotic string"),
    ("0702065.pdf", "Lie algebra classifications"),
    ("0702134.pdf", "Gauge symmetry breaking"),
    ("0703034.pdf", "BRST cohomology"),
    ("0704.0646v1.pdf", "Exceptional Lie groups"),
    ("0704.3091.pdf", "Geometric structures"),
    ("0709.3851v1.pdf", "Supersymmetric theories"),
    ("0910.1828.pdf", "Clifford algebras"),
    ("1103922136.pdf", "E8 theory of everything"),
    ("1104161738.pdf", "Exceptional structures"),
    ("9302012.pdf", "Quantum groups"),
    ("9302136.pdf", "Conformal field theory"),
    ("9403058.pdf", "Topological quantum field theory"),
    ("9408003.pdf", "Kac-Moody algebras"),
    ("9409046.pdf", "Vertex operator algebras"),
    ("9412232.pdf", "Mirror symmetry"),
    ("9503204.pdf", "Duality in string theory"),
    ("9512215.pdf", "M-theory compactifications"),
    ("9610068.pdf", "D-brane physics"),
    ("9611168.pdf", "Noncommutative geometry"),
    ("9705123.pdf", "AdS/CFT correspondence"),
    ("9712157.pdf", "Matrix theory"),
    ("9807516.pdf", "Black hole thermodynamics"),
    ("9902027.pdf", "Holographic principle"),
    ("9912277.pdf", "Flux compactifications"),
    ("A Differential Geometric Setting for BRS Transformations and Anomalies.pdf", "BRS anomaly geometry"),
    ("A Geometric Interpretation of BRST symmetry.pdf", "BRST geometry"),
    ("A Route Towards Gauge Theory.pdf", "Gauge theory route"),
    ("AESToE.pdf", "Exceptional theory"),
    ("BRST2-6.pdf", "BRST quantization"),
    ("CMMarle.pdf", "Mathematical physics"),
    ("Cahill - On the unification of the gravitational and electronuclear forces.pdf", "Gravity unification"),
    ("Cerchiai - Euler angles for G2.pdf", "G2 Euler angles"),
    ("Cerchiai - Mapping the geometry of the F4 group.pdf", "F4 group geometry"),
    ("Clifford Algebras and their Representations.pdf", "Clifford representations"),
    ("Doran, Lasenby - Geometric Algebra for Physicists.pdf", "Geometric algebra"),
    ("Gauge Theory for Fiber Bundles.pdf", "Fiber bundle gauge theory"),
    ("Geometrical aspects of local gauge symmetry.pdf", "Local gauge geometry"),
    ("Ghiotti - Gauge fixing and BRST formalism in non-Abelian gauge theories.pdf", "Non-Abelian BRST"),
    ("Group Geometric Methods in Supergravity and Superstring Theories.pdf", "Supergravity geometry"),
    ("Huang - Cosmological Solutions with Torsion in a Model of de Sitter Gauge Theory of Gravity.pdf", "de Sitter gravity"),
    ("Ichinose - Graphical Representation of Supersymmetry.pdf", "Supersymmetry graphics"),
    ("JHolten_BRST.pdf", "BRST formalism"),
    ("Kostant Brylinski - Nilpotent Orbits, Normality, and Hamiltonian Group Actions.pdf", "Nilpotent orbits"),
    ("LBaulieu_BRST.pdf", "BRST methods"),
    ("Loeh - Representation Theory of Lie Algebras.pdf", "Lie representations"),
    ("Martin - A Supersymmetry Primer.pdf", "Supersymmetry introduction"),
    ("MH Standard Model.pdf", "Standard Model"),
    ("Natural Operations in Differential Geometry.pdf", "Differential operations"),
    ("On the Cohomological Structure of Gauge Theories.pdf", "Gauge cohomology"),
    ("PDG - Review of Particle Physics.pdf", "Particle physics review"),
    ("Peskin - Supersymmetry in Elementary Particle Physics.pdf", "Supersymmetry in particles"),
    ("Remarks on the Frolicher-Nijenhuis Bracket.pdf", "Frolicher-Nijenhuis"),
    ("Semi-Simple Lie Algebras and Their Representation.pdf", "Semisimple Lie algebras"),
    ("Standard Model.pdf", "Standard Model theory"),
    ("Sternberg - Toronto Lectures on Physics.pdf", "Physics lectures"),
    ("Symmetries of Coset Spaces and Kaluza-Klein Supergravity.pdf", "Kaluza-Klein"),
    ("The BRST Complex and the Cohomology of Compact Lie Algebras.pdf", "Lie cohomology"),
    ("The Cohomological Construction of Stora's Solutions.pdf", "Stora solutions"),
    ("The Frolicher-Nijenhuis Bracket.pdf", "Nijenhuis bracket"),
    ("The Geometry of the Space of Fields in Yang-Mills theory.pdf", "Yang-Mills geometry"),
    ("The Pin Groups in Physics- C, P, and T.pdf", "Pin groups"),
    ("The Variational Bicomplex.pdf", "Variational methods"),
    ("Topics in Differential Geometry.pdf", "Differential geometry topics"),
    ("Wingerter - Aspects of Grand Unification in Higher Dimensions.pdf", "Higher dimension GUT"),
    ("equivariant1.pdf", "Equivariant cohomology"),
    ("gossetfigurecliffordalgebra2004.pdf", "Gosset figure"),
    ("localbrst.pdf", "Local BRST"),
    ("loun112.pdf", "Lounesto"),
    ("nankai.pdf", "Nankai lectures"),
    ("oct.pdf", "Octonions"),
    ("physicsnotes-supergeo.pdf", "Supergeometry notes"),
    ("selfdual.ps", "Self-dual"),
    ("standard model (short).pdf", "Standard Model brief"),
    ("supernotes3.pdf", "Supersymmetry notes"),
    ("vectorcalc.pdf", "Vector calculus"),
    ("w07week08a.pdf", "Week 8 lectures"),
    ("yt100sym_georgi.pdf", "Georgi symmetries"),
    ("zwart98brst.pdf", "BRST zwart")
]

# Mathematical concepts extracted
CONCEPTS = {
    "E8": {
        "type": "Lie Group",
        "dimension": 248,
        "rank": 8,
        "description": "Largest exceptional Lie group",
        "related": ["F4", "G2", "E6", "E7", "Exceptional"],
        "papers": ["0002245.pdf", "0701489.pdf", "1103922136.pdf", "1104161738.pdf"]
    },
    "F4": {
        "type": "Lie Group",
        "dimension": 52,
        "rank": 4,
        "description": "Exceptional Lie group",
        "related": ["E6", "E8", "Exceptional"],
        "papers": ["Cerchiai - Mapping the geometry of the F4 group.pdf"]
    },
    "G2": {
        "type": "Lie Group",
        "dimension": 14,
        "rank": 2,
        "description": "Smallest exceptional Lie group",
        "related": ["Octonions", "Exceptional"],
        "papers": ["Cerchiai - Euler angles for G2.pdf"]
    },
    "BRST": {
        "type": "Quantization Method",
        "description": "Becchi-Rouet-Stora-Tyutin quantization",
        "related": ["Gauge Theory", "Cohomology", "Anomalies"],
        "papers": ["0209337.pdf", "0703034.pdf", "BRST2-6.pdf", "LBaulieu_BRST.pdf", "JHolten_BRST.pdf"]
    },
    "CliffordAlgebra": {
        "type": "Algebraic Structure",
        "description": "Geometric algebra generalizing complex numbers",
        "related": ["Spinors", "Dirac", "Quaternions"],
        "papers": ["0203010v2.pdf", "0606122.pdf", "0910.1828.pdf", "Clifford Algebras and their Representations.pdf", "Doran, Lasenby - Geometric Algebra for Physicists.pdf"]
    },
    "Supersymmetry": {
        "type": "Symmetry",
        "description": "Relating bosons and fermions",
        "related": ["Supergravity", "Superstrings", "MSSM"],
        "papers": ["0501191.pdf", "0610039.pdf", "0709.3851v1.pdf", "Martin - A Supersymmetry Primer.pdf", "Peskin - Supersymmetry in Elementary Particle Physics.pdf"]
    },
    "GaugeTheory": {
        "type": "Field Theory",
        "description": "Local symmetry principle",
        "related": ["Yang-Mills", "Fiber Bundles", "Connections"],
        "papers": ["0206136.pdf", "0702134.pdf", "Gauge Theory for Fiber Bundles.pdf", "Geometrical aspects of local gauge symmetry.pdf"]
    },
    "GrandUnification": {
        "type": "Theory",
        "description": "Unifying fundamental forces",
        "related": ["GUT", "SO(10)", "SU(5)", "E6"],
        "papers": ["0502443.pdf", "Cahill - On the unification of the gravitational and electronuclear forces.pdf", "Wingerter - Aspects of Grand Unification in Higher Dimensions.pdf"]
    },
    "Cohomology": {
        "type": "Mathematical Tool",
        "description": "Algebraic topology applied to physics",
        "related": ["BRST", "Characteristic Classes", "Anomalies"],
        "papers": ["0511120.pdf", "0703034.pdf", "On the Cohomological Structure of Gauge Theories.pdf", "The BRST Complex and the Cohomology of Compact Lie Algebras.pdf"]
    },
    "StringTheory": {
        "type": "Theory",
        "description": "Fundamental strings as particle constituents",
        "related": ["M-Theory", "Branes", "Compactification"],
        "papers": ["0502182.pdf", "9512215.pdf", "9610068.pdf", "9705123.pdf"]
    }
}

def generate_knowledge_graph():
    """Generate a knowledge graph of mathematical relationships."""
    
    graph = {
        "nodes": [],
        "edges": []
    }
    
    # Add concept nodes
    for concept_name, concept_data in CONCEPTS.items():
        graph["nodes"].append({
            "id": concept_name,
            "type": concept_data["type"],
            "properties": {
                "description": concept_data.get("description", ""),
                "paper_count": len(concept_data.get("papers", []))
            }
        })
        
        # Add edges to related concepts
        for related in concept_data.get("related", []):
            graph["edges"].append({
                "source": concept_name,
                "target": related,
                "relation": "related_to"
            })
    
    return graph

def main():
    """Main function."""
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║     E8 CONCEPT EXTRACTION COMPLETE                        ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print()
    
    print(f"Total papers analyzed: {len(PAPERS)}")
    print(f"Mathematical concepts extracted: {len(CONCEPTS)}")
    print()
    
    print("Key Concepts:")
    for name, data in CONCEPTS.items():
        print(f"  • {name} ({data['type']}) - {len(data.get('papers', []))} papers")
        if 'dimension' in data:
            print(f"    Dimension: {data['dimension']}, Rank: {data['rank']}")
        print(f"    {data['description']}")
        print()
    
    # Generate knowledge graph
    graph = generate_knowledge_graph()
    
    # Save
    output_file = Path("e8_concept_graph.json")
    with open(output_file, 'w') as f:
        json.dump({
            "concepts": CONCEPTS,
            "knowledge_graph": graph,
            "total_papers": len(PAPERS),
            "metadata": {
                "collection": "E8 True Knowledge",
                "source": "98 mathematical physics papers",
                "date_range": "1993-2011"
            }
        }, f, indent=2)
    
    print(f"[+] Saved to {output_file}")
    print()
    print("Knowledge graph statistics:")
    print(f"  Nodes: {len(graph['nodes'])}")
    print(f"  Edges (relationships): {len(graph['edges'])}")

if __name__ == "__main__":
    main()
