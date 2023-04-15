#!/usr/bin/env python

from mistletoe import Document
from massivewiki import MassiveWikiRenderer

test_strings = [
    [ '[[test]]', '<p><a class="wikilink" href="/test">test</a></p>\n' ],
    [ '[[test|test2]]', '<p><a class="wikilink" href="/test">test2</a></p>\n' ],
    [ '[[test.txt| test2  ]]', '<p><a class="wikilink" href="/test.txt">test2</a></p>\n' ],
    [ '[[test| test2  ]]', '<p><a class="wikilink" href="/test">test2</a></p>\n' ],
    [ '[[test|test2|test3]]', '<p><a class="wikilink" href="/test">test2|test3</a></p>\n' ],
    [ '![[testi1.png]]', '<p><img src="/testi1.png" alt="an image with no alt text" /></p>\n' ],
    [ '![[testi2.png|A Beautiful PNG Image]]', '<p><img src="/testi2.png" alt="A Beautiful PNG Image" /></p>\n' ],
]

for pair in test_strings:
    with MassiveWikiRenderer() as renderer:
        doc = Document(pair[0])
        result = renderer.render(doc)
        print(pair[0], ' ... ', end='')
        if result == pair[1]:
            print('pass')
        else:
            print(f'FAIL\nexpected: »{pair[1]}«\ngot: »{result}«')

