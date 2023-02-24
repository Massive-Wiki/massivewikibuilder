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

def main():
    argparser = init_argparse();
    args = argparser.parse_args();

    # remember paths
    dir_wiki = Path(args.wiki).resolve().as_posix()
    print(dir_wiki)
    rootdir = "/"
    
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
