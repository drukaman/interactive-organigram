#!/usr/bin/env python3
"""
Create a simplified organigram showing only the top 2-3 levels
"""

import csv
import json
from collections import defaultdict

def clean_field(field):
    """Remove quotes and handle NULL values"""
    if field == 'NULL' or field == '':
        return None
    return field.strip('"')

def create_simplified_mermaid():
    """Create a simplified Mermaid diagram with only top levels"""
    nodes = {}
    
    # Read CSV
    with open('nodes.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            node_id = clean_field(row['id'])
            pid = clean_field(row['pid'])
            name = clean_field(row['name'])
            level = clean_field(row['level'])
            
            nodes[node_id] = {
                'id': node_id,
                'name': name,
                'pid': pid,
                'level': level
            }
    
    # Create simplified diagram with only l1 and l2 levels
    mermaid_lines = ["graph TD"]
    added_nodes = set()
    
    # Add l1 nodes (roots)
    l1_nodes = [node for node in nodes.values() if node['level'] == 'l1']
    for node in l1_nodes:
        clean_name = node['name'].replace('"', '').replace("'", "")
        if len(clean_name) > 30:
            clean_name = clean_name[:27] + "..."
        mermaid_lines.append(f'    {node["id"]}["{clean_name}"]')
        added_nodes.add(node['id'])
    
    # Add l2 nodes and their connections
    l2_nodes = [node for node in nodes.values() if node['level'] == 'l2']
    for node in l2_nodes:
        if node['pid'] in added_nodes:  # Only if parent exists
            clean_name = node['name'].replace('"', '').replace("'", "")
            if len(clean_name) > 30:
                clean_name = clean_name[:27] + "..."
            mermaid_lines.append(f'    {node["id"]}["{clean_name}"]')
            mermaid_lines.append(f'    {node["pid"]} --> {node["id"]}')
            added_nodes.add(node['id'])
    
    return "\n".join(mermaid_lines)

def main():
    # Create simplified Mermaid diagram
    print("Creating simplified Mermaid diagram...")
    mermaid_content = create_simplified_mermaid()
    
    # Save simplified Mermaid file
    with open('organigram_simple.mmd', 'w', encoding='utf-8') as f:
        f.write(mermaid_content)
    
    print("Created organigram_simple.mmd")
    
    # Create HTML file for the simplified diagram
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Simplified Nodes Organigram</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .mermaid {{ max-width: 100%; overflow-x: auto; }}
        h1 {{ color: #333; }}
        .info {{ background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>Simplified Nodes Organigram (Top 2 Levels)</h1>
    
    <div class="info">
        <h3>About this diagram:</h3>
        <p>This shows the hierarchical structure of nodes with only the top 2 levels (l1 and l2) for better readability.</p>
        <p>The complete hierarchy has 4 levels with 11,754 nodes total:</p>
        <ul>
            <li>Level 1: 7 root nodes</li>
            <li>Level 2: 71 nodes</li>
            <li>Level 3: 2,935 nodes</li>
            <li>Level 4: 8,741 nodes</li>
        </ul>
    </div>
    
    <div class="mermaid">
{mermaid_content}
    </div>
    
    <script>
        mermaid.initialize({{ 
            startOnLoad: true,
            theme: 'default',
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true
            }}
        }});
    </script>
</body>
</html>"""
    
    with open('organigram_simple.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Created organigram_simple.html")

if __name__ == "__main__":
    main()
