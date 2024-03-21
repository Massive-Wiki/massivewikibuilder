"""
Massive Wiki support for mistletoe.
"""
# set up logging
import logging, os
logging.basicConfig(level=os.environ.get('LOGLEVEL', 'WARNING').upper())

from itertools import chain
from mistletoe import Document
from mistletoe.span_token import SpanToken
from mistletoe.html_renderer import HTMLRenderer
from pathlib import Path
import html
import re

__all__ = ['DoubleSquareBracketLink', 'EmbeddedImageDoubleSquareBracketLink', 'TranscludedDoubleSquareBracketLink', 'MassiveWikiRenderer']

class DoubleSquareBracketLink(SpanToken):
    """
    Defines double square bracket link (span).
    """
    pattern = re.compile(r"\[\[ *(.+?) *(\| *.+?)? *\]\]")

    def __init__(self, match):
        if match.group(2):
            self.target = re.sub(r"^\| *", '', match.group(2), count=1)
        else:
            self.target = match.group(1)

class EmbeddedImageDoubleSquareBracketLink(SpanToken):
    """
    Defines embedded image double square bracket link (span).
    """
    pattern = re.compile(r"\!\[\[ *(.+?)\.(png|jpg|jpeg|gif|svg|webp) *(\| *.+?)? *\]\]")
    
    def __init__(self, match):
        # get alt text into target and filename into content
        self.content = match.group(1) + '.' + match.group(2)
        if match.group(3):
            self.target = re.sub(r"^\| *", '', match.group(3), count=1)
        else:
            self.target = ''

class TranscludedDoubleSquareBracketLink(SpanToken):
    """
    Defines double square bracket link (span) for Markdown note transclusion
    """
    pattern = re.compile(r"!\[\[ *([^.|\]]+?)\]\]")

    def __init__(self, match):
        self.target = match.group(1)

class MassiveWikiRenderer(HTMLRenderer):
    """
    Extends HTMLRenderer to handle double square bracket links.

    Args:
        rootdir (string): directory path to prepend to all links, defaults to '/'.
        fileroot (string): local filesystem path to the root of the wiki, so we can read transcluded pages.

    Properties:
        links (array of strings, read-only): all of the double square bracket link targets found in this invocation.
    """
    def __init__(self, rootdir='/', fileroot='.', wikilinks={}, file_id=''):
        super().__init__(*chain([TranscludedDoubleSquareBracketLink,EmbeddedImageDoubleSquareBracketLink,DoubleSquareBracketLink]))
        self._rootdir = rootdir
        self._fileroot = fileroot
        self._wikilinks = wikilinks
        self._file_id = file_id
        self._tc_dict = dict.fromkeys([self._file_id], [])
        self._tc_dict[self._file_id].append(self._file_id)

    def render_double_square_bracket_link(self, token):
        logging.debug("WIKILINKED token: %s", token)
        target = token.target
        logging.debug("WIKILINKED token.target: %s", token.target)
        logging.debug("WIKILINKED inner(token): %s", self.render_inner(token))
        wikilink_key = html.unescape(Path(self.render_inner(token)).name).lower()
        logging.debug("WIKILINKED wikilink_key: %s", wikilink_key)
        wikilink_value = self._wikilinks.get(wikilink_key, None)
        logging.debug("WIKILINKED wikilink_value: %s", wikilink_value)
        if wikilink_value:
            inner = Path(wikilink_value['html_path']).relative_to(self._rootdir).as_posix()
            template = '<a class="wikilink" href="{rootdir}{inner}">{target}</a>'
        else:
            inner = self.render_inner(token)
            template = '<span class="incipient-wikilink">{target}</span>'
        logging.debug("WIKILINKED inner: %s", inner)
        return template.format(target=target, inner=inner, rootdir=self._rootdir)

    def render_embedded_image_double_square_bracket_link(self, token):
        logging.debug("EMBEDDED token: %s", token)
        template = '<img src="{rootdir}{inner}" alt="{target}" />'
        target = token.target
        if not target:
            target = "an image with no alt text"
        logging.debug("EMBEDDED token.target: %s", token.target)
        logging.debug("EMBEDDED token.content: %s", token.content)
        logging.debug("EMBEDDED inner(token): %s", self.render_inner(token))
        wikilink_key = token.content.lower()
        wikilink_value = self._wikilinks.get(wikilink_key, None)
        logging.debug("EMBEDDED wikilink_key: %s", wikilink_key)
        logging.debug("EMBEDDED wikilink_value: %s", wikilink_value)
        if wikilink_value:
            inner = Path(wikilink_value['html_path']).relative_to(self._rootdir).as_posix()
        else:
            inner = token.content
        logging.debug("EMBEDDED inner: %s", inner)
        return template.format(target=target, inner=inner, rootdir=self._rootdir)

    def render_transcluded_double_square_bracket_link(self, token):
        logging.debug("TRANSCLUDED file_id: %s", self._file_id)
        logging.debug("TRANSCLUDED fileroot: %s", self._fileroot)        
        logging.debug("TRANSCLUDED token: %s", token)
        target = token.target
        logging.debug("TRANSCLUDED token.target: %s", token.target)
        inner = self.render_inner(token)
        logging.debug("TRANSCLUDED inner(token): %s", self.render_inner(token))
        wikilink_key = html.unescape(Path(self.render_inner(token)).name).lower()
        logging.debug("TRANSCLUDED wikilink_key: %s", wikilink_key)
        wikilink_value = self._wikilinks.get(wikilink_key, None)
        logging.debug("TRANSCLUDED wikilink_value: %s", wikilink_value)
        if wikilink_value:
            logging.debug("TRANSCLUDED wikipage_id: %s", wikilink_value['wikipage_id'])
            if any(wikilink_value['wikipage_id'] in x for x in self._tc_dict[self._file_id]):
                logging.debug("*** ruh roh! there is a transclude loop")
                template = '<p><span class="transclusion-error">Cannot transclude <strong>{inner}</strong> within itself.</span></p>'
            else:
                self._tc_dict[self._file_id].append(wikilink_value['wikipage_id'])
                logging.debug("TRANSCLUDED _tc_dict: %s", self._tc_dict)
                transclude_path = f"{self._fileroot}{wikilink_value['fs_path']}"
                logging.debug(f"TRANSCLUDED loading contents of '{transclude_path}'")
                with open(transclude_path, 'r') as infile: inner = infile.read()
                rendered_doc = self.render(Document(inner))
                htmlpath = wikilink_value['html_path']
                template = f'<p><a href="{htmlpath}" style="float:right">🔗</a> {rendered_doc} </p>'
        else:
            template = '<p><span class="transclusion-error">TRANSCLUSION {target} NOT FOUND</span></p>'
        logging.debug("TRANSCLUDED inner: %s", inner[:50])
        return template.format(target=target, inner=inner, rootdir=self._rootdir)

