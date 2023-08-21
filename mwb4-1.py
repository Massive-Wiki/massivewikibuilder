#!/usr/bin/env python3

import os
import shutil
import logging
import argparse
import re
import sys
from mistletoe import markdown, span_token
from mistletoe.span_token import SpanToken
from mistletoe.html_renderer import HTMLRenderer
from jinja2 import Environment, FileSystemLoader

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WikiLinkToken(SpanToken):
    pattern = re.compile(r'\[\[(.+?)\]\]')
    
    def __init__(self, match_obj):
        self.link = match_obj.group(1)

class WikiLinkRenderer(HTMLRenderer):
    def __init__(self, existing_files):
        super().__init__()
        self.existing_files = existing_files
        
    def render_wiki_link_token(self, token):
        if f"{token.link}.md" in self.existing_files:
            return f'<a href="{token.link}.html">{token.link}</a>'
        else:
            return f'<div class="incipient_link">{token.link}</div>'

# Register our WikiLinkToken with mistletoe
span_token.add_token(WikiLinkToken, 0)

def copy_files(src_dir, dest_dir):
    """
    Copy files and directory hierarchy from src_dir to dest_dir without processing the Markdown files.
    Ignore files or directories that start with a "."
    """
    logging.info("Starting file copy process...")
    for subdir, _, files in os.walk(src_dir):
        if os.path.basename(subdir).startswith('.'):
            logging.info(f"Skipping {subdir}")
            continue
        
        dest_subdir = subdir.replace(src_dir, dest_dir)
        os.makedirs(dest_subdir, exist_ok=True)
        
        for file in files:
            if os.path.basename(file).startswith('.'):
                logging.info(f"Skipping {file}")
                continue
            
            src_filepath = os.path.join(subdir, file)
            dest_filepath = os.path.join(dest_subdir, file)
            
            try:
                shutil.copy2(src_filepath, dest_filepath)
            except Exception as e:
                logging.error(f"Error copying file {src_filepath}: {str(e)}")

def process_markdown_files(dest_dir, existing_files):
    """
    Convert Markdown files to HTML, process them with Jinja2, and save them next to the original file.
    """
    logging.info("Starting Markdown processing...")
    for subdir, _, files in os.walk(dest_dir):
        if '/.' in subdir:
            continue

        for file in files:
            if file.lower().endswith('.md'):
                dest_filepath = os.path.join(subdir, file)
                convert_and_write_html(dest_filepath, existing_files)
                
def convert_and_write_html(dest_filepath, existing_files):
    """
    Convert Markdown file to HTML, process it with Jinja2, and write it next to the original file.
    """
    logging.info(f"Processing Markdown file: {dest_filepath}")
    try:
        with open(dest_filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            markdown_body = markdown(content, WikiLinkRenderer(existing_files))
        
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template('page.html')
        
        html_content = template.render(markdown_body=markdown_body)
        
        html_filepath = os.path.splitext(dest_filepath)[0] + '.html'
        with open(html_filepath, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)
            
    except Exception as e:
        logging.error(f"Error processing file {dest_filepath}: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Markdown files to HTML and copy files to a new directory.")
    parser.add_argument('-i', '--input', required=True, help="Input directory containing the files")
    parser.add_argument('-o', '--output', required=True, help="Output directory where files will be copied")
    parser.add_argument('-t', '--templates', required=True, help="Template directory containing the Jinja2 templates")
    
    args = parser.parse_args()
    
    src_directory = args.input
    dest_directory = args.output
    template_dir = args.templates

    logging.info("Script started")
    logging.info(f"Input Directory: {src_directory}")
    logging.info(f"Output Directory: {dest_directory}")
    logging.info(f"Template Directory: {template_dir}")

    copy_files(src_directory, dest_directory)

    logging.info("File copy process completed")

    # Get the list of existing Markdown files in the output directory to validate Wiki links
    existing_files = set()
    for subdir, _, files in os.walk(dest_directory):
        if '/.' in subdir:
            continue

        for file in files:
            existing_files.add(file)
            
    process_markdown_files(dest_directory, existing_files)

    logging.info("Script completed successfully")
