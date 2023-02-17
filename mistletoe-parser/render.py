#!/usr/bin/env python

import sys

from mistletoe import Document
from massivewiki import MassiveWikiRenderer

for filename in sys.argv[1:]:
    with open(filename, 'r') as infile:
        with MassiveWikiRenderer(rootdir="/test/") as renderer:
            doc = Document(infile.readlines())
            result = renderer.render(doc)
            print(f"links={renderer.links}\n")
            print(result)
