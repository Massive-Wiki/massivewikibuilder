# Link workbench

These are a set of pages that help us think through and test wiki link handling, both for [[Massive Wiki Builder]], and Massive Wiki in general.

See:
- [[Massive Wiki Builder wikilinks specification]]
- [Enhancement request: switchable transformation for page filename to slug · Issue \#34](https://github.com/peterkaminski/massivewikibuilder/issues/34)
- other files in this directory

Concepts include:

- page name - the title of the page, used in wiki links
	- filename - when the wiki is stored in a filesystem, the name of the file that contains the page
- slug - the page identifier, usually a transformation of the page name / filename, used for a page's URL
- filename mangling - the process of turning an arbitrary filename into a URL-compliant slug. less frequently, might refer to transformations from page name to file name, respecting filesystem limitations on characters or length. more usually, a filesystem-based wiki will prevent people from creating page titles that cannot also be file names.

## Other systems

- [HedgeDoc will not be a wiki](https://github.com/hedgedoc/react-client/issues/443#issuecomment-762491225), and related matters - possible wiki link syntaxes, URL safety, Unicode issues.
- FedWiki:
	- <https://github.com/fedwiki/wiki-client/blob/3e0a1dd499b5eb637eeb4a03970c9f0a4310e619/lib/page.coffee#L17-L18>
	- [Beyond Slugs](http://ward.asia.wiki.org/view/beyond-slugs) (ward.asia.wiki.org)
