# Massive Wiki Builder

Massive Wiki Builder is a static site generator for turning [Massive Wikis](https://massive.wiki/) into static HTML websites.

## Typical Hierarchy

Typically, there is a `.massivewikibuilder` directory, which contains `massivewikibuilder` (this repo), and other related files and directories.

The `.` character is important when the MWB workspace directory is within the wiki itself.  MWB ignores dotfiles and dot-directories, so as it builds, it will ignore anything inside (for instance) `.obsidian` or `.massivewikibuilder` directories.  If you don't have it set up this way, MWB will continue to try to copy and convert the files in the output directory, and it will start an infinite loop, which will stop when the directory names get too long.

```
--/ # root of wiki directories
---- .massivewikibuilder/ # MWB workspace
------ mwb.yaml # config for this wiki
------ massivewikibuilder/ # MWB
------ massive-wiki-themes/ # off-the-shelf themes, not customized
-------- alto/ # a specific theme, customized for this wiki
------ this-wiki-themes/ # theme(s) used for this wiki
-------- alto/ # a specific theme, customized for this wiki
------ output/ # MWB writes .html, .md, and .json files here
```

Note that MWB removes (if necessary) and recreates the `output` directory each time it is run.

## Static Files

Note: Prior to v1.9.0, MWB handled static files slightly differently. If `mwb-static` existed, it copied it from the theme directory to the output directory. Starting with v1.9.0, it will still do this, but it will output a warning, `WARNING:root:WARNING:root:mwb-static is deprecated, please use 'static'`. The warning is meant to suggest that you should move `mwb-static` into the `static` directory at the top level of the theme.  `static` is described below.

After the HTML pages are built from the Markdown files, if a directory named `static` exists at the top level of the theme, all the files and directories within it are copied to the root of the output directory.  By convention, static files such as CSS, JavaScript, and images are put in a directory inside `static` called `mwb-static`. Favicon files and other files that should be at the root of the website are put at the root of `static`.

The name `static` is used in the theme because it's descriptive, and won't collide with anything in the wiki. (The _content_ of `static` is copied, but not `static` itself.)

The `mwb-static` convention is used to contain static files used by the wiki, and instead of `static`, it is named `mwb-static` so it is less likely to collide with a wiki directory with the same name. (In contrast to `static` in the theme, `mwb-static` itself _is_ copied to the output directory, where all the wiki files and directories live.)

In the theme:

```
--/ # root of theme
---- static/ # anything in here is copied to the root of the output
------ favicon.ico # for instance, favicon.ico
------ mwb-static/ # static files and subdirectories that don't need to be at the root of the website
-------- css/
-------- js/
-------- images/
```

Results in the output website:

```
--/ # root of website
--- favicon.ico # for instance, favicon.ico
---- mwb-static/ # static files and subdirectories that don't need to be at the root of the website
------ css/
------ js/
------ images/
```

Side note about favicon files; it is suggested to use a favicon generator such as [RealFaviconGenerator](https://realfavicongenerator.net/) to create the various icon files needed for different platforms. This note is meant for informational purposes, and does not represent an endorsement of RealFaviconGenerator in particular.

## Install

(not yet completed)
(remember to `pip install -r requirements.txt`)

(clone massive-wiki-themes repo, call it massive-wiki-themes)

## Build

In `.massivewikibuilder/`:

```shell
./mwb.py -c mwb.yaml -w .. -o output -t massive-wiki-themes/alto
```

If you want to print a log what's happening during the build, set the `LOGLEVEL` environment variable to `DEBUG`.

On the command line, do:

```shell
LOGLEVEL=DEBUG ./mwb.py -c mwb.yaml -w .. -o output -t massive-wiki-themes/alto
```

or:

```shell
export LOGLEVEL=DEBUG
./mwb.py -c mwb.yaml -w .. -o output -t massive-wiki-themes/alto
```

In `netlify.toml`, do:

```toml
[build.environment]
  LOGLEVEL = "DEBUG"
```



## Deploy (Netlify)

For Netlify deploys, you can include a `netlify.toml` file like this at the root of your repo:

```toml
[build]
  ignore = "/bin/false"
  base = ".massivewikibuilder"
  publish = "output"
  command = "./mwb.py -c mwb.yaml -w .. -o output -t massive-wiki-themes/alto"

[build.environment]
  PYTHON_VERSION = "3.8"
```



## Develop

Because static assets have an absolute path, you may want to start a local web server while you're developing and testing.  Change to the output directory and run this command:

```
python3 -m http.server
```

## Themes

MWB uses a simple theming system.  All the files for one theme are placed in a subdirectory in the themes directory, usually `massive-wiki-themes`.  For example, the Alto theme is in `massive-wiki-themes/alto`, and to use the Alto theme, pass `-t massive-wiki-themes/alto` to MWB.

MWB builds the pages with Jinja2, so you can use Jinja2 directives within the HTML files to include wiki metadata and wiki content.  You can also use the Jinja2 `include` functionality to extract reused parts of the page to HTML "partial" files.

Themes are in a separate repo, [github/peterkaminski/massive-wiki-themes](https://github.com/peterkaminski/massive-wiki-themes).

