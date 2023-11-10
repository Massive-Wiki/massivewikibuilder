"""
Massive Wiki support for mistletoe.
"""
# set up logging
import logging, os
logging.basicConfig(level=os.environ.get('LOGLEVEL', 'WARNING').upper())

from itertools import chain
from mistletoe.span_token import SpanToken
from mistletoe.html_renderer import HTMLRenderer
from pathlib import Path
import html
import re

__all__ = ['DoubleSquareBracketLink', 'EmbeddedImageDoubleSquareBracketLink', 'MassiveWikiRenderer']


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

class MassiveWikiRenderer(HTMLRenderer):
    """
    Extends HTMLRenderer to handle double square bracket links.

    Args:
        rootdir (string): directory path to prepend to all links, defaults to '/'.

    Properties:
        links (array of strings, read-only): all of the double square bracket link targets found in this invocation.
    """
    def __init__(self, rootdir='/', wikilinks={}):
        super().__init__(*chain([DoubleSquareBracketLink,EmbeddedImageDoubleSquareBracketLink]))
        self._rootdir = rootdir
        self._wikilinks = wikilinks

    def render_double_square_bracket_link(self, token):
        target = token.target
        logging.debug("token.target: %s", token.target)
        logging.debug("inner(token): %s", self.render_inner(token))
        wikilink_key = html.unescape(Path(self.render_inner(token)).name).lower()
        logging.debug("wikilink_key: %s", wikilink_key)
        wikilink_value = self._wikilinks.get(wikilink_key, None)
        logging.debug("wikilink_value: %s", wikilink_value)
        if wikilink_value:
            inner = Path(wikilink_value['html_path']).relative_to(self._rootdir).as_posix()
            template = '<a class="wikilink" href="{rootdir}{inner}">{target}</a>'
        else:
            inner = self.render_inner(token)
            template = '<span class="incipient-wikilink">{target}</span>'
        logging.debug("inner: %s", inner)
        return template.format(target=target, inner=inner, rootdir=self._rootdir)

    def render_embedded_image_double_square_bracket_link(self, token):
        template = '<img src="{rootdir}{inner}" alt="{target}" />'
        target = token.target
        if not target:
            target = "an image with no alt text"
        logging.debug("token.target: %s", token.target)
        logging.debug("token.content: %s", token.content)
        logging.debug("inner(token): %s", self.render_inner(token))
        wikilink_key = token.content
        wikilink_value = self._wikilinks.get(wikilink_key, None)
        logging.debug("wikilink_key: %s", wikilink_key)
        logging.debug("wikilink_value: %s", wikilink_value)
        if wikilink_value:
            inner = Path(wikilink_value['html_path']).relative_to(self._rootdir).as_posix()
        else:
            inner = token.content
        logging.debug("inner: %s", inner)
        return template.format(target=target, inner=inner, rootdir=self._rootdir)
