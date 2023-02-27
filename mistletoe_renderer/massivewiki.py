"""
Massive Wiki support for mistletoe.
"""

import re
from mistletoe.span_token import SpanToken
from mistletoe.html_renderer import HTMLRenderer


__all__ = ['MassiveWiki', 'MassiveWikiRenderer']


class MassiveWiki(SpanToken):
    """
    Defines double square bracket link (span).
    """
    pattern = re.compile(r"\[\[ *(.+?) *(\| *.+?)? *\]\]")

    def __init__(self, match):
        if match.group(2):
            self.target = re.sub(r"^\| *", '', match.group(2), count=1)
        else:
            self.target = match.group(1)

class MassiveWikiRenderer(HTMLRenderer):
    """
    Extends HTMLRenderer to handle double square bracket links.

    Args:
        rootdir (string): directory path to prepend to all links, defaults to '/'.

    Properties:
        links (array of strings, read-only): all of the double square bracket link targets found in this invocation.
    """
    def __init__(self, rootdir='/'):
        super().__init__(MassiveWiki)
        self._links = []
        self._rootdir = rootdir

    @property
    def links(self):
        return self._links

    def render_massive_wiki(self, token):
        template = '<a class="wikilink" href="{rootdir}{inner}">{target}</a>'
        target = self.escape_url(token.target)
        inner = self.render_inner(token)
        self._links.append(target)
        return template.format(target=target, inner=inner, rootdir=self._rootdir)
