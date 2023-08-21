# mwb4.py

import os
import sys
import re
import argparse
import shutil
from mistletoe import Document
from jinja2 import Environment, FileSystemLoader
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s', stream=sys.stderr)

def copy_files(input_dir, output_dir, wiki_links):
    """
    Traverse through the input directory and copy files to the output directory.
    Record wiki links in Markdown files.
    """
    for root, _, files in os.walk(input_dir):
        # Ignore hidden directories
        if os.path.basename(root).startswith('.'):
            continue
        
        # Create corresponding directories in the output directory
        rel_path = os.path.relpath(root, input_dir)
        new_dir = os.path.join(output_dir, rel_path)
        os.makedirs(new_dir, exist_ok=True)
        
        for file in files:
            # Ignore hidden files
            if os.path.basename(file).startswith('.'):
                continue
            
            src_path = os.path.join(root, file)
            dest_path = os.path.join(new_dir, file)
            
            # Copy the file to the output directory
            shutil.copy2(src_path, dest_path)
            
            # Check for Markdown files and record wiki links
            if file.lower().endswith('.md'):
                with open(src_path, 'r') as md_file:
                    content = md_file.read()
                    wiki_links_in_file = set([link[2:-2] for link in re.findall(r'\[\[.*?\]\]', content)])
                    wiki_links.update(wiki_links_in_file)
                    
def render_html(input_dir, output_dir, template_dir, wiki_links):
    """
    Convert Markdown to HTML, process wiki links, and render HTML using Jinja2 templates.
    """
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('page.html')
    
    for root, _, files in os.walk(input_dir):
        # Ignore hidden directories
        if os.path.basename(root).startswith('.'):
            continue
        
        rel_path = os.path.relpath(root, input_dir)
        new_dir = os.path.join(output_dir, rel_path)
        
        for file in files:
            # Ignore hidden files
            if os.path.basename(file).startswith('.'):
                continue
            
            if file.lower().endswith('.md'):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(new_dir, file[:-3] + '.html')
                
                with open(src_path, 'r') as md_file:
                    content = md_file.read()
                    markdown_body = Document(content).html
                
                # Process Wiki Links
                for link in wiki_links:
                    if link in content:
                        if link + '.md' in files:
                            markdown_body = markdown_body.replace('[[{}]]'.format(link), '<a href="{}.html">{}</a>'.format(link, link))
                        else:
                            markdown_body = markdown_body.replace('[[{}]]'.format(link), '<div class="incipient_link">{}</div>'.format(link))
                
                # Render HTML
                html_content = template.render(markdown_body=markdown_body)
                
                # Save HTML file
                with open(dest_path, 'w') as html_file:
                    html_file.write(html_content)

def main():
    parser = argparse.ArgumentParser(description='Convert a directory of Markdown files into a structured collection of HTML files.')
    parser.add_argument('-i', '--input', required=True, help='Input directory containing Markdown files.')
    parser.add_argument('-o', '--output', required=True, help='Output directory to save HTML files.')
    parser.add_argument('-t', '--templates', required=True, help='Directory containing HTML templates.')
    
    args = parser.parse_args()
    input_dir = args.input
    output_dir = args.output
    template_dir = args.templates
    
    # Ensure the input directory exists
    if not os.path.isdir(input_dir):
        logging.error('Input directory does not exist.')
        sys.exit(1)
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Store all wiki links found in Markdown files
    wiki_links = set()
    
    # Step 1: Copy files and record wiki links
    copy_files(input_dir, output_dir, wiki_links)
    
    # Step 2: Render HTML files
    render_html(input_dir, output_dir, template_dir, wiki_links)

if __name__ == '__main__':
    main()
