#!/usr/bin/env python

import mistletoe
from massivewiki import MassiveWikiRenderer

test_strings = [
    [ '[[test]]', '<p><a class="wikilink" href="test">test</a></p>\n' ],
    [ '[[test|test2]]', '<p><a class="wikilink" href="test2">test</a></p>\n' ],
    [ '[[test| test2  ]]', '<p><a class="wikilink" href="test2">test</a></p>\n' ],
    [ '[[test| test2  ]]', '<p><a class="wikilink" href="test2">test</a></p>\n' ],
    [ '[[test|test2|test3]]', '<p><a class="wikilink" href="test2%7Ctest3">test</a></p>\n' ],
]

for pair in test_strings:
    result = mistletoe.markdown(pair[0], MassiveWikiRenderer)
    print(pair[0], ' ... ', end='')
    if result == pair[1]:
        print('pass')
    else:
        print(f'FAIL\nexpected: »{pair[1]}«\ngot: »{result}«')

