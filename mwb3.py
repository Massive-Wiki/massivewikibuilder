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

# markdown processing
from mistletoe import Document
from mistletoe_renderer.massivewiki import MassiveWikiRenderer

# set up argparse
def init_argparse():
    parser = argparse.ArgumentParser(description='Generate HTML pages from Markdown wiki pages.')
    parser.add_argument('--config', '-c', required=True, help='path to YAML config file')
    parser.add_argument('--output', '-o', required=True, help='directory for output')
    parser.add_argument('--templates', '-t', required=True, help='directory for HTML templates')
    parser.add_argument('--wiki', '-w', required=True, help='directory containing wiki files (Markdown + other)')
    parser.add_argument('--lunr', action='store_true', help='include this to create lunr index (requires npm and lunr to be installed, read docs)')
    parser.add_argument('--commits', action='store_true', help='include this to read Git commit messages and times, for All Pages')
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

# mistletoe based Markdown to HTML conversion -- WIKILINKS NOT YET WORKING
def markdown_convert(markdown_text):
    with MassiveWikiRenderer() as renderer:
        return renderer.render(Document(markdown_text))

# read and convert Sidebar markdown to HTML
def sidebar_convert_markdown(path):
    if path.exists():
        markdown_text, front_matter = read_markdown_and_front_matter(path)
    else:
        markdown_text = ''
    return markdown_convert(markdown_text)

# handle datetime.date serialization for json.dumps()
def datetime_date_serializer(o):
    if isinstance(o, datetime.date):
        return o.isoformat()

def main():
    logging.debug("Initializing")
    
    argparser = init_argparse()
    args = argparser.parse_args()
    logging.debug("args: %s", args)

    # get configuration
    config = load_config(args.config)
    if not 'recent_changes_count' in config:
        config['recent_changes_count'] = 5

    # remember paths
    dir_output = Path(args.output).resolve().as_posix()
    dir_templates = Path(args.templates).resolve().as_posix()
    dir_wiki = Path(args.wiki).resolve().as_posix()
    rootdir = '/'

    # get a Jinja2 environment
    j = jinja2_environment(dir_templates)

    # set up lunr_index_filename and lunr_index_sitepath
    if (args.lunr):
        timestamp_thisrun = time.time()
        lunr_index_filename = f"lunr-index-{timestamp_thisrun}.js" # needed for next two variables
        lunr_index_filepath = Path(dir_output) / lunr_index_filename # local filesystem
        lunr_index_sitepath = '/'+lunr_index_filename # website
        lunr_posts_filename = f"lunr-posts-{timestamp_thisrun}.js" # needed for next two variables
        lunr_posts_filepath = Path(dir_output) / lunr_posts_filename # local filesystem
        lunr_posts_sitepath = '/'+lunr_posts_filename # website
    else:
        # needed to feed to themes
        lunr_index_sitepath = ''
        lunr_posts_sitepath = ''

    # render the wiki
    try:
        # remove existing output directory and recreate
        logging.debug("remove existing output directory and recreate")
#        shutil.rmtree(dir_output, ignore_errors=True)
#        os.mkdir(dir_output)
    
        # read wiki content and build wikilinks, lunr index lists, and all_pages list    
        wikilinks = {}
        all_pages = []
        if(args.lunr):
            lunr_idx_data=[]
            lunr_posts=[]

        # run through all files, construct wikilink dict, copy to output
        # build list of files using a glob.iglob iterator
        allfiles = [f for f in glob.iglob(f"{dir_wiki}/**/*.*", recursive=True, include_hidden=False)]
        for f in allfiles:
            logging.debug("file %s: ", f)
            if Path(f).suffix == '.md':
                print("key: ", Path(f).name)
                html_path = re.sub(r'([ _?\#]+)', '_', rootdir+Path(f).relative_to(dir_wiki).with_suffix(".html").as_posix())
                print("html path: ", html_path, "\n")
                # append path and link to wikilinks dict
                wikilinks[Path(f).stem] = html_path
                # add lunr data to lunr idx_data and posts lists
                if(args.lunr):
                    pass
                # add wikipage to all_pages list
            else:
                print("key: ", Path(f).name)
                html_path = re.sub(r'([ _?\#]+)', '_', rootdir+Path(f).relative_to(dir_wiki).as_posix())
                print("html path: ", html_path, "\n")
                # add path and link to wikilinks dict
                wikilinks[Path(f).name] = html_path
        logging.debug("wikilinks: %s", wikilinks)
        # shutil.copy(Path(root) / file, Path(dir_output) / path / clean_name)

        # render all the Markdown files
        for f in allfiles:
            if Path(f).suffix == '.md':
                print(f"Rendering {f}")

        # done
        logging.debug("done")
    
    except FileNotFoundError as e:
        print(f"\n{e}\n\nCheck that arguments specify valid files and directories.\n")
    except Exception as e:
        traceback.print_exc(e)

if __name__ == "__main__":
    exit(main())
