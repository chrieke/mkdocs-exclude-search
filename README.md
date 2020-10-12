# mkdocs-exclude-search

A mkdocs plugin that lets you exclude selected files or header sections from the search index.

## Setup

Install the plugin using pip:

`pip install mkdocs-exclude-search`

Activate the plugin in `mkdocs.yml`:
```yaml
plugins:
  - search
  - exclude-search
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [MkDocs documentation][mkdocs-plugins].

## Config

List the files to be excluded from the search as they appear in the `mkdocs.yml` nav 
section. You can also only exclude specific heading subsections.

```yaml
plugins:
  - search
  - exclude-search:
      files:
        - second.md
        - third.md#some-heading

```
```yaml
nav:
    - Home: index.md
    - First chapter: first.md
    - Second chapter: second.md
    - Third chapter: third.md
```

This example would display all three chapters, but would exclude from the search, the 
second chapter completely and the `some-heading` header subsection of the third chapter 
from.


## See Also

More information about templates [here][mkdocs-template].

More information about blocks [here][mkdocs-block].

[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[mkdocs-template]: https://www.mkdocs.org/user-guide/custom-themes/#template-variables
[mkdocs-block]: https://www.mkdocs.org/user-guide/styling-your-docs/#overriding-template-blocks
