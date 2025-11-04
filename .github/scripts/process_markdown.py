#!/usr/bin/env python3
"""
Script to process markdown files before syncing to deploy branch.

This script:
1. Removes YAML frontmatter description sections from MD files
2. Converts level 2 titles to level 1 titles in SUMMARY.md
3. Removes <figure></figure> HTML elements but keeps content inside
"""

import os
import re
import sys
from pathlib import Path


def remove_yaml_frontmatter(content):
    """Remove YAML frontmatter from markdown content."""
    # Match YAML frontmatter at the beginning of the file
    pattern = r'^---\n.*?\n---\n'
    return re.sub(pattern, '', content, flags=re.DOTALL | re.MULTILINE)


def process_summary_titles(content):
    """Convert level 2 titles (##) to level 1 titles (#) in SUMMARY.md."""
    # Replace ## with #
    return re.sub(r'^## ', '# ', content, flags=re.MULTILINE)


def remove_figure_tags(content):
    """Remove <figure></figure> HTML elements but keep the content inside."""
    # Remove opening <figure> tags (with any attributes)
    content = re.sub(r'<figure[^>]*>', '', content)
    
    # Remove closing </figure> tags
    content = re.sub(r'</figure>', '', content)
    
    # Clean up any extra whitespace that might be left
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    return content


def process_markdown_file(file_path):
    """Process a single markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all transformations
        content = remove_yaml_frontmatter(content)
        content = remove_figure_tags(content)
        
        # Special processing for SUMMARY.md
        if file_path.name == 'SUMMARY.md':
            content = process_summary_titles(content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Processed: {file_path}")
            return True
        else:
            print(f"No changes: {file_path}")
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def find_markdown_files(src_dir):
    """Find all markdown files in the src directory."""
    src_path = Path(src_dir)
    if not src_path.exists():
        print(f"Source directory {src_dir} does not exist")
        return []
    
    markdown_files = list(src_path.rglob('*.md'))
    return markdown_files


def main():
    """Main function to process all markdown files."""
    # Get the repository root directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent
    src_dir = repo_root / 'src'
    
    print(f"Repository root: {repo_root}")
    print(f"Source directory: {src_dir}")
    
    # Find all markdown files
    markdown_files = find_markdown_files(src_dir)
    
    if not markdown_files:
        print("No markdown files found to process")
        return 0
    
    print(f"Found {len(markdown_files)} markdown files to process")
    
    # Process each file
    processed_count = 0
    for file_path in markdown_files:
        if process_markdown_file(file_path):
            processed_count += 1
    
    print(f"Successfully processed {processed_count} files")
    return 0


if __name__ == '__main__':
    sys.exit(main())