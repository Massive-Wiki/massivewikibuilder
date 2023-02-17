#!/usr/bin/env python

from mistletoe import Document
from massivewiki import MassiveWikiRenderer

test_strings = [
    [ '[[test]]', '<p><a class="wikilink" href="test">test</a></p>\n' ],
    [ '[[test|test2]]', '<p><a class="wikilink" href="test2">test</a></p>\n' ],
    [ '[[test| test2  ]]', '<p><a class="wikilink" href="test2">test</a></p>\n' ],
    [ '[[test| test2  ]]', '<p><a class="wikilink" href="test2">test</a></p>\n' ],
    [ '[[test|test2|test3]]', '<p><a class="wikilink" href="test2%7Ctest3">test</a></p>\n' ],
]

for pair in test_strings:
    with MassiveWikiRenderer() as renderer:
        doc = Document(pair[0])
        result = renderer.render(doc)
        print(f"links={renderer.links}")
        print(pair[0], ' ... ', end='')
        if result == pair[1]:
            print('pass')
        else:
            print(f'FAIL\nexpected: »{pair[1]}«\ngot: »{result}«')

