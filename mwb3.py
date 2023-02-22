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
