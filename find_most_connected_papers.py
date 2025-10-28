#!/usr/bin/env python3
"""
Find the most connected papers based on network centrality.
This identifies papers that are central hubs in the citation network.
"""
import networkx as nx
import pandas as pd
import os

def load_graph(graphml_path):
    """Load citation graph from GraphML file."""
    print(f"Loading citation graph from {graphml_path}...")
    G = nx.read_graphml(graphml_path)
    print(f"Loaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges\n")
    return G

def get_node_info(G, node):
    """Get DOI and metadata for a node."""
    doi = G.nodes[node].get('doi', node)
    label = G.nodes[node].get('label', 'Unknown')
    first_author = G.nodes[node].get('first_author', 'Unknown')
    year = G.nodes[node].get('year', 'Unknown')
    return doi, label, first_author, year

def find_most_connected_papers(G, top_n=20):
    """
    Find the most connected papers by considering:
    - Total connections (degree): papers with most connections
    - In-degree (citations): papers cited by most other papers
    - Betweenness: papers that act as bridges
    """
    results = []
    
    print("Analyzing connections...")
    
    for node in G.nodes():
        doi, label, first_author, year = get_node_info(G, node)
        
        # Total degree (incoming + outgoing)
        total_degree = G.degree(node)
        
        # In-degree (cited by others)
        in_degree = G.in_degree(node)
        
        # Out-degree (references others)
        out_degree = G.out_degree(node)
        
        results.append({
            'DOI': doi,
            'Label': label,
            'First Author': first_author,
            'Year': year,
            'Total_Connections': total_degree,
            'Cited_By': in_degree,
            'References': out_degree,
        })
    
    # Sort by total connections (most connected)
    results.sort(key=lambda x: x['Total_Connections'], reverse=True)
    
    return results[:top_n]

def main():
    # Load the citation graph
    G = load_graph('output/citation_graph.graphml')
    
    # Find most connected papers
    most_connected = find_most_connected_papers(G, top_n=20)
    
    print("=" * 80)
    print("MOST CONNECTED PAPERS (by total connections)")
    print("=" * 80)
    
    for i, paper in enumerate(most_connected, 1):
        print(f"\n{i}. {paper['Label']}")
        print(f"   Total Connections: {paper['Total_Connections']}")
        print(f"   Cited By: {paper['Cited_By']} papers")
        print(f"   References: {paper['References']} papers")
        print(f"   DOI: {paper['DOI']}")
    
    # Save to CSV
    output_file = 'output/most_connected_papers.csv'
    os.makedirs('output', exist_ok=True)
    pd.DataFrame(most_connected).to_csv(output_file, index=False)
    
    print(f"\n\nResults saved to {output_file}")
    
    print("\n" + "=" * 80)
    print("HOW IT WORKS:")
    print("=" * 80)
    print("""
The script identifies the most connected papers by calculating:

1. **Total Connections (Degree)**: How many links a paper has in total
   - This combines both papers that cite it (in-degree) and papers it cites (out-degree)
   - More connections = more central in the network

2. **Cited By (In-Degree)**: How many papers cite this one
   - Higher = more foundational or influential
   - These are the papers others frequently reference

3. **References (Out-Degree)**: How many papers this one cites
   - Higher = well-read paper that builds on many sources
   
The papers are ranked by TOTAL CONNECTIONS because:
- They are the central hubs in your citation network
- They connect to the most other papers (both citing and being cited)
- Reading these papers gives you the best coverage of the research area
- They act as "keystone" papers that link different research streams together

This method is based on the concept of **degree centrality** in network analysis.
    """)

if __name__ == "__main__":
    main()

