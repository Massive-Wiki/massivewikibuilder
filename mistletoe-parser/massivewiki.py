"""
Massive Wiki support for mistletoe.
"""

import re
from mistletoe.span_token import SpanToken
from mistletoe.html_renderer import HTMLRenderer


__all__ = ['MassiveWiki', 'MassiveWikiRenderer']


class MassiveWiki(SpanToken):
    pattern = re.compile(r"\[\[ *(.+?) *(\| *.+?)? *\]\]")

    def __init__(self, match):
        if match.group(2):
            self.target = re.sub(r"^\| *", '', match.group(2), count=1)
        else:
            self.target = match.group(1)

class MassiveWikiRenderer(HTMLRenderer):
    def __init__(self):
        super().__init__(MassiveWiki)

    def render_massive_wiki(self, token):
        template = '<a class="wikilink" href="{target}">{inner}</a>'
        target = self.escape_url(token.target)
        inner = self.render_inner(token)
        return template.format(target=target, inner=inner)
