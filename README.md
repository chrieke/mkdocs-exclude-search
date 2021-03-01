# mkdocs-exclude-search

A mkdocs plugin that lets you exclude selected files or sections from the search index.

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

- List the markdown files to be excluded under `exclude` using the format `<path>/<to>/filename.md` in the docs folder.
- Exclude specific heading subsections using the format `<path>/<to>/filename.md#some-heading`. Chapter names are all lowercase, `-` as separator, no spaces.
- Exclude all markdown files within a directory (and its children) with `dirname/*.md` or `dirname/*`.
- To still include a subsection of an excluded file, list the subsection heading under `ignore` using the format `<path>/<to>/filename.md#some-heading`. 

```yaml
plugins:
  - search
  - exclude-search:
      exclude:
        - second.md
        - third.md#some-heading  
        - dir/*.md
        - dir2/sub/*.md
      ignore:
        - second.md#another-heading

```
```yaml
nav:
    - Home: index.md
    - First chapter: first.md
    - Second chapter: second.md
    - Third chapter: third.md
    - Fourth chapter: some_directory/fourth.md
```

This example would exclude:
- the second chapter (but still include its `another-heading` subsection) 
- the `some-heading` subsection of the third chapter.
- all markdown files within `dir` and `dir2/sub` (and their children).



## See Also

More information about templates [here][mkdocs-template].

More information about blocks [here][mkdocs-block].

[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[mkdocs-template]: https://www.mkdocs.org/user-guide/custom-themes/#template-variables
[mkdocs-block]: https://www.mkdocs.org/user-guide/styling-your-docs/#overriding-template-blocks
