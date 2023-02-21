#!/usr/bin/env python

import argparse
import glob
import os
from pathlib import Path
import re

# set up logging
import logging
logging.basicConfig(level=os.environ.get('LOGLEVEL', 'WARNING').upper())

# set up argparse
def init_argparse():
    parser = argparse.ArgumentParser(description='Generate HTML pages from Markdown wiki pages.')
    parser.add_argument('--wiki', '-w', required=True, help='directory containing wiki files (Markdown + other)')
    return parser

def main():
    argparser = init_argparse();
    args = argparser.parse_args();

    # remember paths
#    dir_wiki = os.path.abspath(args.wiki)
    dir_wiki = Path(args.wiki).resolve().as_posix()
    print(dir_wiki)
    rootdir = "/"
    
    # mdfiles
    mdfiles = [f for f in glob.glob(f"{dir_wiki}/**/*.md", recursive=True, include_hidden=False)] # TODO: consider adding .txt
    for mdfile in mdfiles:
        print(mdfile)
#        print(mdfile.replace(dir_wiki, ''), "\n")
        print(rootdir+Path(mdfile).relative_to(dir_wiki).as_posix(), "\n")
        print(re.sub(r'([ _?\#]+)', '_', rootdir+Path(mdfile).relative_to(dir_wiki).with_suffix(".html").as_posix()), "\n")

if __name__ == "__main__":
    exit(main())
