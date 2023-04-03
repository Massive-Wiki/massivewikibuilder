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
    with MassiveWikiRenderer(rootdir='/',wikilinks=wikilinks) as renderer:
        return renderer.render(Document(markdown_text))

#def markdown_convert(markdown_text):
#    with MassiveWikiRenderer() as renderer:
#        return renderer.render(Document(markdown_text))

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

wikilinks ={}

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
        shutil.rmtree(dir_output, ignore_errors=True)
        os.mkdir(dir_output)
    
        # read wiki content and build wikilinks dictionary; lunr index lists
#        wikilinks = {}
        if(args.lunr):
            lunr_idx_data=[]
            lunr_posts=[]
        
        # get list of files using a glob.iglob iterator (consumed in list comprehension)
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

        # render all the Markdown files
        logging.debug("copy wiki to output; render .md files to HTML")
        all_pages = []
        page = j.get_template('page.html')
        build_time = datetime.datetime.now(datetime.timezone.utc).strftime("%A, %B %d, %Y at %H:%M UTC")

        if 'sidebar' in config:
            sidebar_body = sidebar_convert_markdown(Path(dir_wiki) / config['sidebar'])
        else:
            sidebar_body = ''

        for file in allfiles:
            # TODO: refactor Path(file) --? used in several places
            clean_filepath = scrub_path(rootdir+Path(file).relative_to(dir_wiki).as_posix())
            # make needed subdirectories
            os.makedirs(Path(dir_output+clean_filepath).parent, exist_ok=True)
            if Path(file).suffix == '.md':
                print(f"Rendering {file}")
                # parse Markdown file
                markdown_text, front_matter = read_markdown_and_front_matter(Path(file))
                if front_matter is False:
                    print(f"NOTE: YAML syntax error in front matter of '{Path(file)}'")
                    front_matter = {}
                # output JSON of front matter
                (Path(dir_output+clean_filepath).with_suffix(".json")).write_text(json.dumps(front_matter, indent=2, default=datetime_date_serializer))
                # render and output HTML
                markdown_body = markdown_convert(markdown_text)
                html = page.render(
                    build_time=build_time,
                    wiki_title=config['wiki_title'],
                    author=config['author'],
                    repo=config['repo'],
                    license=config['license'],
                    title=Path(file).stem,
                    markdown_body=markdown_body,
                    sidebar_body=sidebar_body,
                    lunr_index_sitepath=lunr_index_sitepath,
                    lunr_posts_sitepath=lunr_posts_sitepath,
                )
                (Path(dir_output+clean_filepath).with_suffix(".html")).write_text(html)
                
                # get commit message and time
                if args.commits:
                    p = subprocess.run(["git", "-C", Path(root), "log", "-1", '--pretty="%cI\t%an\t%s"', file], capture_output=True, check=True)
                    (date,author,change)=p.stdout.decode('utf-8')[1:-2].split('\t',2)
                    date = parse(date).astimezone(datetime.timezone.utc).strftime("%Y-%m-%d, %H:%M")
                else:
                    date = ''
                    change = ''
                    author = ''

                    # remember this page for All Pages
                    all_pages.append({
                        'title':Path(file).stem,
                        'path':"/"+scrub_path(Path(file).relative_to(dir_wiki).with_suffix('.html').as_posix()),
                        'date':date,
                        'change':change,
                        'author':author,
                    })
            # copy all original files
            date,change,author = '','','' # MWB3 TESTING PHASE ONLY
            logging.debug("Copy all original files")
            logging.debug("%s -->  %s",Path(file), Path(dir_output+clean_filepath))
            shutil.copy(Path(file), Path(dir_output+clean_filepath))

        # copy README.html to index.html if no index.html
        logging.debug("copy README.html to index.html if no index.html")
        if not os.path.exists(Path(dir_output) / 'index.html'):
            shutil.copyfile(Path(dir_output) / 'README.html', Path(dir_output) / 'index.html')

        # copy static assets directory
        logging.debug("copy static assets directory")
        if os.path.exists(Path(dir_templates) / 'mwb-static'):
            logging.warning("mwb-static is deprecated. please use 'static', and put mwb-static inside static - see docs")
            shutil.copytree(Path(dir_templates) / 'mwb-static', Path(dir_output) / 'mwb-static')
        if os.path.exists(Path(dir_templates) / 'static'):
            shutil.copytree(Path(dir_templates) / 'static', Path(dir_output), dirs_exist_ok=True)

        # build all-pages.html
        logging.debug("build all-pages.html")
        if args.commits:
            all_pages_chrono = sorted(all_pages, key=lambda i: i['date'], reverse=True)
        else:
            all_pages_chrono = ''
        all_pages = sorted(all_pages, key=lambda i: i['title'].lower())
        html = j.get_template('all-pages.html').render(
            build_time=build_time,
            pages=all_pages,
            pages_chrono=all_pages_chrono,
            wiki_title=config['wiki_title'],
            author=config['author'],
            repo=config['repo'],
            license=config['license'],
            lunr_index_sitepath=lunr_index_sitepath,
            lunr_posts_sitepath=lunr_posts_sitepath,
        )
        (Path(dir_output) / "all-pages.html").write_text(html)

        # done
        logging.debug("done")
    
    except FileNotFoundError as e:
        print(f"\n{e}\n\nCheck that arguments specify valid files and directories.\n")
    except Exception as e:
        traceback.print_exc(e)

if __name__ == "__main__":
    exit(main())
