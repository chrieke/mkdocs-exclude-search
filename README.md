# mkdocs-exclude-search

A mkdocs plugin that lets you exclude selected files or sections from the search index.

<p align="center">
    <a href="https://pypi.org/project/mkdocs-exclude-search/" title="mkdocs-exclude-search on pypi"><img src="https://img.shields.io/pypi/v/mkdocs-exclude-search?color=brightgreen"></a>
    <img src="./coverage.svg">
</p>

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
- Exclude all markdown files within a directory (and its children) with `dirname/*`.
- Exclude all markdown files with a specific name within all subdirectories with `dirname/*/filename.md` or `/*/filename.md`.    
- To still include a subsection of an excluded file, list the subsection heading under `ignore` using the format `<path>/<to>/filename.md#some-heading`. 

```yaml
plugins:
  - search
  - exclude-search:
      exclude:
        - first.md
        - dir/second.md
        - third.md#some-heading
        - dir2/*
        - /*/fifth.md
      ignore:
        - dir/second.md#some-heading

```
```yaml
nav:
    - Home: index.md
    - First chapter: first.md
    - Second chapter: dir/second.md
    - Third chapter: third.md
    - Fourth chapter: dir2/fourth.md
    - Fifth chapter: subdir/fifth.md
```

This example would exclude:
- the first chapter.
- the second chapter (but still include its `some-heading` section).
- the `some-heading` section of the third chapter.
- all markdown files within `dir2` (and its children directories).
- all markdown files named `fifth.md` within all subdirectories.

## See Also

More information about templates [here][mkdocs-template].

More information about blocks [here][mkdocs-block].

[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[mkdocs-template]: https://www.mkdocs.org/user-guide/custom-themes/#template-variables
[mkdocs-block]: https://www.mkdocs.org/user-guide/styling-your-docs/#overriding-template-blocks
