# mkdocs-exclude-search

A mkdocs plugin that lets you exclude selected chapters from the search index.

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

List the chapters to be excluded from the search as they appear in the `mkdocs.yml` nav section.
This example would display all three chapters, but only include the first chapter in the search.

```yaml
plugins:
  - search
  - exclude-search:
      chapters:
        - Second Chapter
        - Third Chapter
```

```yaml
nav:
    - Home: index.md
    - First Chapter: first-chapter.md
    - Second Chapter: second-chapter.md
    - Third Chapter: third-chapter.md
```

## See Also

More information about templates [here][mkdocs-template].

More information about blocks [here][mkdocs-block].

[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[mkdocs-template]: https://www.mkdocs.org/user-guide/custom-themes/#template-variables
[mkdocs-block]: https://www.mkdocs.org/user-guide/styling-your-docs/#overriding-template-blocks
