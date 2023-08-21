from mistletoe.span_token import SpanToken
from mistletoe.html_renderer import HTMLRenderer
from mistletoe.block_token import Paragraph
import re

# Step 1: Define new token classes for our custom spans

class WikiLinkToken(SpanToken):
    def __init__(self, match_obj):
        self.link = match_obj.group(1)

class TextWikiLinkToken(SpanToken):
    def __init__(self, match_obj):
        self.text = match_obj.group(1)
        self.link = match_obj.group(2)

class ImageToken(SpanToken):
    def __init__(self, match_obj):
        self.src = match_obj.group(1)

# Step 2: Integrate Custom Spans into Mistletoe's Parsing Process

class CustomParagraph(Paragraph):
    def __init__(self, lines):
        super().__init__(lines)
        self.parse_spans()
        
    def parse_spans(self):
        wiki_link_pattern = re.compile(r'\[\[(.*?)\]\]')
        text_wiki_link_pattern = re.compile(r'\[\[(.*?)/(.*?)\]\]')
        image_pattern = re.compile(r'!\[\[(.*?\.(?:jpg|png|gif|bmp|webp|jpeg|svg))\]\]')
        
        for i, child in enumerate(self.children):
            if isinstance(child, str):
                self.children[i:i+1] = self.tokenize(child, wiki_link_pattern, text_wiki_link_pattern, image_pattern)
                
    @staticmethod
    def tokenize(line, wiki_link_pattern, text_wiki_link_pattern, image_pattern):
        tokens = []
        pos = 0
        for match in wiki_link_pattern.finditer(line):
            tokens.append(line[pos:match.start()])
            tokens.append(WikiLinkToken(match))
            pos = match.end()
        for match in text_wiki_link_pattern.finditer(line):
            tokens.append(line[pos:match.start()])
            tokens.append(TextWikiLinkToken(match))
            pos = match.end()
        for match in image_pattern.finditer(line):
            tokens.append(line[pos:match.start()])
            tokens.append(ImageToken(match))
            pos = match.end()
        tokens.append(line[pos:])
        return tokens

# Step 3: Extend the existing HTML renderer to handle our new token class

class CustomHTMLRenderer(HTMLRenderer):
    def __init__(self, rootdir, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rootdir = rootdir

    def render_wiki_link_token(self, token):
        return f'<a href="/{self.rootdir}/{token.link}.html">{token.link}</a>'
    
    def render_text_wiki_link_token(self, token):
        return f'<a href="/{self.rootdir}/{token.link}.html">{token.text}</a>'
    
    def render_image_token(self, token):
        return f'<img src="/{self.rootdir}/{token.src}">'
    
    def render_str(self, text):
        return text

# Testing the custom renderer
markdown_input = '''
[[Wiki Link]]
[[Link Text/Wiki Link]]
![[Image Filename.jpg]]
'''

# Instantiate custom renderer with a root directory
renderer = CustomHTMLRenderer('rootdir')

# Render the Markdown input using our custom renderer
html_output = renderer.render(markdown_input)
print(html_output)
