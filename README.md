# Massive Wiki Builder

Massive Wiki Builder is a static site generator for turning [Massive Wikis](https://massive.wiki/) into static HTML websites.

Typically, it is installed at the root of the wiki, next to all the top-level Markdown files, in a subdirectory named `.massivewikibuilder`.

The `.` character is important when the MWB directory is within the wiki itself.  MWB ignores dotfiles and dot-directories, so as it builds, it will ignore anything inside (for instance) `.obsidian` or `.massivewikibuilder` directories.  If you don't have it set up this way, MWB will continue to try to copy and convert the files in the output directory, and it will start an infinite loop, which will stop when the directory names get too long.

## Typical Hierarchy

```
--/ # root of wiki directories
---- .massivewikibuilder/ # MWB and its input/output
------ output/ # MWB writes .html, .md, and .json files here
------ themes/ # all the themes
-------- alto/ # a specific theme
```

Note that MWB removes (if necessary) and recreates the `output` directory each time it is run.

## Install

(not yet completed)
(remember to `pip install -r requirements.txt`)

## Build

In `.massivewikibuilder/`:

```
./mwb.py -w .. -o output -t themes/alto
```

## Develop

Because static assets have an absolute path, you may want to start a local web server while your developing and testing.  Change to the output directory and run this command:

```
python3 -m http.server
```

## Themes

MWB uses a simple theming system.  All the files are placed in subdirectory in the `themes` directory.

MWB builds the pages with Jinja2, so you can use Jinja2 directives within the HTML files to include wiki metadata and wiki content.  You can also use the Jinja2 `include` functionality to extract reused parts of the page to HTML "partial" files.

These themes are included in this repo:

- Alto - a simple but nice responsive theme, implemented with [Bulma](https://bulma.io).  It would be fairly easy to add more Bulma components to the pages.
- Skeleton - a straightforward, plain HTML theme, demonstrating a minimally viable theme.  It uses `include` functionality for a navbar and footer.
- Super Skeleton - the bare minimum, even more minimal than Skeleton; not even includes.
