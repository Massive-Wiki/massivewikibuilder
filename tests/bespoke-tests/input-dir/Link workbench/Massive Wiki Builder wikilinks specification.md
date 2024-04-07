# MWB wikilinks specification?

see more about wiki links, filenames, and URLs at [[Link workbench]].

(question mark missing from filename because Netlify doesn't like `?` or `#` in deployed filenames.)

(Or something like a specification? use RFC template?)

/ outline the syntax //
/ do not assume scheme when encountering ':' (Obsidian does not allow ':' in file names, so such links cannot create wiki pages) //
/ generate full path links from root of the wiki //
/ do not change case on the text in the link //

```

for each line
  find wikilink string
  (e.g., with this re: wikilink_pattern="\[\[(.*?)\]\]")

search wikifiles dictionary
  if found replace string with wikilink full pathname


```

#### 2022-05-12
wikilink edge cases (from Pete)
```
-   [[wiki page]]
-   [[Wiki Page]]
-   [[wikI pagE]]
-   [[WikiPage]]
-   [[../wiki page]]
-   [[../../wiki page]]
-   [[../subdir/wiki page]]
-   [[/wiki page]]
-   [[/subdir/wiki page]]
-   [[/subdir/../subdir2/../wiki page]]
-   [[wiki page.md]]
-   [[wiki page.jpg]]
-   [[wiki page.jpeg]]
-   [[wiki page.bmp]]
-   [[wiki page/]]
-   [[wiki page.exe]]
-   [[wiki page.txt]]
-   [[Page: Wiki]]
-   [[Punctuation Is !@#$%^&*()_+-={}[]|\:";'<>,.?/~` Fun]]

```

build first tests for a small set of ordinary cases that
1. do not have identical wiki page basenames in links to different pages
2. can have "/" in the links
3. have case-sensitive basenames

```
-   [[wiki page1]]
-   [[../wiki page2]]
-   [[../../wiki page3]]
-   [[../subdir/wiki page4]]
-   [[/wiki page5]]
-   [[/subdir/wiki page6]]
-   [[/subdir/../subdir2/../wiki page7]]
-
```


#### 2022-05-22
- need to handle ".txt" files (also other media and document files) explicitly, perhaps the same way as image files; or
- perhaps build a way to create wikilinks for any file that is *not* a Markdown files with ".md" extension?

### 2022-05-23

Pete's guess at workflow for wikilinks, including wikilinks with paths:

- walk the wiki, find all the filenames, lowercase the filename, and save the filepath to the file to a dictionary
- when processing each page and converting wikilinks to HTML links:
	- if a target string (starts with any `.` or `/` characters) or (includes a `/`  character anywhere), just append `.html` to the target to create the HTML link, and emit a diagnostic message that the link was not transformed in anyway, because it contained path-like characters (`./`).
	- otherwise, lowercase the target string, then use it as a key to look up the filepath in the dictionary. Append `.html` to the filepath, and use that to create the HTML link

Design principles:

- don't try to process path characters, because handling a complicated path is complicated (e.g., `foo/../../bar/../baz`), and we don't (yet) want to promise users we will do it correctly.  instead, just pass along any target that looks like it is trying to include path characters (even if the path would be invalid).
- at least for now, minimize the code required to handle links, to make it easier to write and maintain.
- make links case-insensitive, by lowercasing wiki links and generated filenames.

Examples:

- foobar -> foobar.html
- FooBar -> foobar.html
- Foobar -> foobar.html
- foo bar -> foo bar.html
- foo/bar -> foo/bar.html
- ./foobar -> ./foobar.html
- .foobar -> .foobar.html (may not work properly, as designed)
- foobar/ -> foobar/.html (may not work properly, as designed)
- /foo/bar/baz -> /foo/bar/baz.html
