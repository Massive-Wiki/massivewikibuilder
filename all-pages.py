#!/usr/bin/env python

# all-pages.py - print all page names as wikilinks, hacked from MWB v1.3.3

import argparse
import os
import re
import traceback

from pathlib import Path

# set up argparse
def init_argparse():
    parser = argparse.ArgumentParser(description='Print all page names as wikilinks.')
    parser.add_argument('--wiki', '-w', required=True, help='directory containing wiki files (Markdown + other)')
    return parser

def main():
    argparser = init_argparse();
    args = argparser.parse_args();

    # remember paths
    dir_wiki = os.path.abspath(args.wiki)

    # walk the directory and find files
    try:
        # copy wiki to output; render .md files to HTML
        for root, dirs, files in os.walk(dir_wiki):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]
            readable_path = root[len(dir_wiki)+1:]
            path = re.sub(r'([ ]+_)|(_[ ]+)|([ ]+)', '_', readable_path)
            for file in files:
                clean_name = re.sub(r'([ ]+_)|(_[ ]+)|([ ]+)', '_', file)
                if file.lower().endswith('.md'):
                    print(f"- [[{readable_path}/{file[:-3]}]]")

    except Exception as e:
        traceback.print_exc(e)

if __name__ == "__main__":
    exit(main())
