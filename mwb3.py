#!/usr/bin/env python

# Massive Wiki Builder v3.0.0

# set up logging
import logging, os
logging.basicConfig(level=os.environ.get('LOGLEVEL', 'WARNING').upper())

# python libraries
import argparse
import datetime
import glob
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import traceback

# pip install
from dateutil.parser import parse # pip install python-dateutil
import jinja2
import yaml

# set up argparse
def init_argparse():
    parser = argparse.ArgumentParser(description='Generate HTML pages from Markdown wiki pages.')
#    parser.add_argument('--config', '-c', required=True, help='path to YAML config file')
#    parser.add_argument('--output', '-o', required=True, help='directory for output')
#    parser.add_argument('--templates', '-t', required=True, help='directory for HTML templates')
    parser.add_argument('--wiki', '-w', required=True, help='directory containing wiki files (Markdown + other)')
#    parser.add_argument('--lunr', action='store_true', help='include this to create lunr index (requires npm and lunr to be installed, read docs)')
#    parser.add_argument('--commits', action='store_true', help='include this to read Git commit messages and times, for All Pages')
    return parser


# set up a Jinja2 environment
def jinja2_environment(path_to_templates):
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path_to_templates)
    )

# load config file
def load_config(path):
    with open(path) as infile:
        return yaml.safe_load(infile)

# scrub wiki path to handle ' ', '_', '?', and '#' characters in wiki page names
# change ' ', ?', and '#' to '_', because they're inconvenient in URLs
def scrub_path(filepath):
    return re.sub(r'([ _?\#]+)', '_', filepath)

# take a path object pointing to a Markdown file
# return Markdown (as string) and YAML front matter (as dict)
# for YAML, {} = no front matter, False = YAML syntax error
def read_markdown_and_front_matter(path):
    with path.open() as infile:
        lines = infile.readlines()
    # take care to look exactly for two `---` lines with valid YAML in between
    if lines and re.match(r'^---$',lines[0]):
        count = 0
        found_front_matter_end = False
        for line in lines[1:]:
            count += 1
            if re.match(r'^---$',line):
                found_front_matter_end = True
                break;
        if found_front_matter_end:
            try:
                front_matter = yaml.safe_load(''.join(lines[1:count]))
            except yaml.parser.ParserError:
                # return Markdown + False (YAML syntax error)
                return ''.join(lines), False
            # return Markdown + front_matter
            return ''.join(lines[count+1:]), front_matter
    # return Markdown + empty dict
    return ''.join(lines), {}

# read and convert Sidebar markdown to HTML
def sidebar_convert_markdown(path):
    if path.exists():
        markdown_text, front_matter = read_markdown_and_front_matter(path)
    else:
        markdown_text = ''
    return markdown.convert(markdown_text)

# handle datetime.date serialization for json.dumps()
def datetime_date_serializer(o):
    if isinstance(o, datetime.date):
        return o.isoformat()

def main():
    argparser = init_argparse();
    args = argparser.parse_args();

    # remember paths
    dir_wiki = Path(args.wiki).resolve().as_posix()
    print(dir_wiki)
    rootdir = "/"
    
    # read wiki content and build wikilinks, lunr index lists, and all_pages list    

    # run through all files, construct wikilink dict, copy to output
    allfiles = [f for f in glob.glob(f"{dir_wiki}/**/*.*", recursive=True, include_hidden=False)]
    for file in allfiles:
        print(file)
        print("key: ", Path(file).name)
        print("web path: ", re.sub(r'([ _?\#]+)', '_', rootdir+Path(file).relative_to(dir_wiki).with_suffix(".html").as_posix()), "\n")
        # shutil.copy(Path(root) / file, Path(dir_output) / path / clean_name)

    # render all the Markdown files
    mdfiles = [f for f in glob.glob(f"{dir_wiki}/**/*.md", recursive=True, include_hidden=False)] # TODO: consider adding .txt
    for mdfile in mdfiles:
        pass
#        print(f"Rendering {mdfile}")

if __name__ == "__main__":
    exit(main())
