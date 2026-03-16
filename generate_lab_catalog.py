#!/usr/bin/env python3
"""
Generate a CSV catalog of all lab markdown files in the Instructions folder.

This script analyzes all .md files in the Instructions folder (recursively),
extracts lab information, and generates a CSV file with:
- File name
- Description
- Technologies/Products
- Last merge date
- Last merge author
"""

import os
import re
import csv
import subprocess
from pathlib import Path
from datetime import datetime


def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown content."""
    # Match YAML frontmatter between --- delimiters
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        frontmatter = match.group(1)
        # Extract title and description (handle both quoted and unquoted values)
        title_match = re.search(r"title:\s*['\"]?(.+?)['\"]?\s*$", frontmatter, re.MULTILINE)
        desc_match = re.search(r"description:\s*['\"]?(.+?)['\"]?\s*$", frontmatter, re.MULTILINE)
        
        title = title_match.group(1).strip().strip("'\"") if title_match else ""
        description = desc_match.group(1).strip().strip("'\"") if desc_match else ""
        
        return title, description
    
    # Fallback: try to extract from first H1 heading
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if h1_match:
        title = h1_match.group(1).strip()
        # Try to extract first paragraph as description
        # Skip the H1 line and look for the first substantial paragraph
        lines = content.split('\n')
        desc_lines = []
        in_content = False
        for line in lines:
            if line.startswith('# '):
                in_content = True
                continue
            if in_content and line.strip() and not line.startswith('#') and not line.startswith('!['):
                # Found a content line (skip image links but not blockquotes)
                desc_lines.append(line.strip())
                full_text = ' '.join(desc_lines)
                # Stop when we have a complete sentence or reach reasonable length
                if len(full_text) > 150 and (full_text.endswith('.') or full_text.endswith('!') or full_text.endswith('?')):
                    break
                elif len(full_text) > 250:
                    # If too long without punctuation, truncate at last complete word
                    full_text = full_text[:250].rsplit(' ', 1)[0]
                    break
        
        description = ' '.join(desc_lines)
        # Truncate at last complete word if too long
        if len(description) > 250:
            description = description[:250].rsplit(' ', 1)[0]
        
        return title, description
    
    return "", ""


def extract_technologies(content):
    """Extract technologies and products mentioned in the lab content."""
    technologies = set()
    
    # Canonical technology names (lowercase keys for matching)
    canonical_names = {
        'azure openai': 'Azure OpenAI',
        'gpt-4o': 'GPT-4o',
        'gpt-4': 'GPT-4',
        'foundry': 'Microsoft Foundry',
        'prompt flow': 'Prompt Flow',
        'rag': 'RAG',
        'retrieval augmented generation': 'Retrieval Augmented Generation',
        'azure ai services': 'Azure AI Services',
        'azure ai studio': 'Azure AI Studio',
        'azure ai foundry': 'Azure AI Foundry',
        'ai hub': 'AI Hub',
        'python sdk': 'Python SDK',
        'typescript': 'TypeScript',
        '.net': '.NET',
        'fine-tune': 'Fine-tuning',
        'fine-tuning': 'Fine-tuning',
        'content filter': 'Content Filters',
        'content filters': 'Content Filters',
        'content filtering': 'Content Filters',
        'evaluation': 'Evaluation',
        'embedding': 'Embeddings',
        'embeddings': 'Embeddings',
        'model catalog': 'Model Catalog',
        'chat app': 'Chat Application',
        'chat application': 'Chat Application',
        'chat playground': 'Chat Playground',
        'ner': 'NER',
        'named entity recognition': 'Named Entity Recognition',
    }
    
    # Common AI/Azure technologies to look for (case-insensitive)
    tech_patterns = [
        r'\bAzure\s+OpenAI\b',
        r'\bGPT-4o?\b',
        r'\bFoundry\b',
        r'\bprompt\s+flow\b',
        r'\bRAG\b',
        r'\bRetrieval\s+Augmented\s+Generation\b',
        r'\bAzure\s+AI\s+(?:Services|Studio|Foundry)\b',
        r'\bAI\s+hub\b',
        r'\bPython\s+SDK\b',
        r'\bTypeScript\b',
        r'\b\.NET\b',
        r'\bfine-tun(?:e|ing)\b',
        r'\bcontent\s+filter(?:s|ing)?\b',
        r'\bevaluation\b',
        r'\bembeddings?\b',
        r'\bmodel\s+catalog\b',
        r'\bchat\s+(?:playground)\b',
        r'\bchat\s+(?:app|application)\b',
        r'\bNER\b',
        r'\bNamed\s+Entity\s+Recognition\b',
    ]
    
    for pattern in tech_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            # Normalize using canonical names
            match_lower = match.lower().strip()
            canonical = canonical_names.get(match_lower, match.strip())
            technologies.add(canonical)
    
    # Return as comma-separated string
    return ", ".join(sorted(technologies)) if technologies else "N/A"


def get_git_info(file_path, repo_root):
    """Get last merge commit date and author for a file."""
    try:
        # Get the relative path from repo root
        rel_path = os.path.relpath(file_path, repo_root)
        
        # Get last commit info for this file (using git log with merges)
        cmd = [
            'git', 'log', '-1', '--merges', '--format=%ai|%an', '--', rel_path
        ]
        result = subprocess.run(
            cmd,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.strip().split('|')
            if len(parts) == 2:
                date_str, author = parts
                # Parse and format the date
                date_obj = datetime.strptime(date_str.split()[0], '%Y-%m-%d')
                return date_obj.strftime('%Y-%m-%d'), author
        
        # If no merge commit found, try regular commits
        cmd = [
            'git', 'log', '-1', '--format=%ai|%an', '--', rel_path
        ]
        result = subprocess.run(
            cmd,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.strip().split('|')
            if len(parts) == 2:
                date_str, author = parts
                # Parse and format the date
                date_obj = datetime.strptime(date_str.split()[0], '%Y-%m-%d')
                return date_obj.strftime('%Y-%m-%d'), author
        
    except Exception as e:
        print(f"Warning: Could not get git info for {file_path}: {e}")
    
    return "N/A", "N/A"


def process_lab_files(repo_root, instructions_dir):
    """Process all markdown lab files and extract information."""
    labs = []
    
    # Find all .md files in Instructions directory
    instructions_path = Path(instructions_dir)
    md_files = sorted(instructions_path.rglob('*.md'))
    
    print(f"Found {len(md_files)} markdown files in {instructions_dir}")
    
    for md_file in md_files:
        print(f"Processing: {md_file}")
        
        try:
            # Read the file content
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract information
            title, description = parse_frontmatter(content)
            technologies = extract_technologies(content)
            last_merge_date, last_merge_author = get_git_info(str(md_file), repo_root)
            
            # Get relative filename from Instructions directory
            rel_filename = md_file.relative_to(instructions_path)
            
            # Combine title and description for the description field
            if title and description:
                # Avoid double punctuation
                separator = ". " if not title.rstrip().endswith(('.', '!', '?')) else " "
                full_description = f"{title}{separator}{description}"
            else:
                full_description = description or title or "N/A"
            
            labs.append({
                'filename': str(rel_filename),
                'description': full_description,
                'technologies': technologies,
                'last_merge_date': last_merge_date,
                'last_merge_author': last_merge_author
            })
            
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
    
    return labs


def generate_csv(labs, output_file):
    """Generate CSV file with lab information."""
    fieldnames = ['filename', 'description', 'technologies', 'last_merge_date', 'last_merge_author']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(labs)
    
    print(f"\nCSV file generated: {output_file}")
    print(f"Total labs documented: {len(labs)}")


def main():
    """Main function to generate the lab catalog."""
    # Get repository root and instructions directory
    repo_root = os.path.dirname(os.path.abspath(__file__))
    instructions_dir = os.path.join(repo_root, 'Instructions')
    output_file = os.path.join(repo_root, 'lab_catalog.csv')
    
    print("="*60)
    print("Lab Catalog Generator")
    print("="*60)
    
    # Process all lab files
    labs = process_lab_files(repo_root, instructions_dir)
    
    # Generate CSV
    generate_csv(labs, output_file)
    
    print("\n" + "="*60)
    print("Done!")
    print("="*60)


if __name__ == '__main__':
    main()
