# mkdocs-exclude-search

A mkdocs plugin that lets you exclude selected files or sections from the search index.

If you only need to exclude a few pages or sections, mkdocs-material now introduced 
[built-in search exclusion](https://squidfunk.github.io/mkdocs-material/setup/setting-up-site-search/#search-exclusion)! 
The **mkdocs-exclude-search** plugin 
[complements](https://squidfunk.github.io/mkdocs-material/blog/2021/09/26/excluding-content-from-search/#whats-new) 
this with more configuration options (wildcard exclusions, ignoring excluded subsections). It also provides 
search-exclusion functionality to regular mkdocs users.

<p align="center">
    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/mkdocs-exclude-search">
    <a href="https://pypi.org/project/mkdocs-exclude-search/" title="mkdocs-exclude-search on pypi"><img src="https://img.shields.io/pypi/v/mkdocs-exclude-search?color=brightgreen"></a>
    <img src="./coverage.svg">
</p>

## Setup

Install the plugin using pip:

```bash
pip install mkdocs-exclude-search
```

**Activate the `search` and `exclude-search` plugins in `mkdocs.yml`**. `search` is required, otherwise 
`exclude-search` has no effect!

```yaml
plugins:
  - search
  - exclude-search
```

More information about plugins in the [MkDocs documentation][mkdocs-plugins].

## Configuration

- List the markdown files to be excluded under `exclude` using the format `<path>/<to>/filename.md` in the docs folder.
- Exclude specific heading subsections using the format `<path>/<to>/filename.md#some-heading`. Chapter names are all lowercase, `-` as separator, no spaces.
- Exclude all markdown files within a directory (and its children) with `dirname/*`.
- Exclude all markdown files with a specific name within all subdirectories with `dirname/*/filename.md` or `/*/filename.md`.    
- To still include a subsection of an excluded file, list the subsection heading under `ignore` using the format `<path>/<to>/filename.md#some-heading`. 
- To exclude all unreferenced files (markdown files not listed in mkdocs.yml nav section), use `exclude_unreferenced: true`. Default false.

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
      exclude_unreferenced: true

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
- all unreferenced files

## See Also

More information about templates [here][mkdocs-template].

More information about blocks [here][mkdocs-block].

[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[mkdocs-template]: https://www.mkdocs.org/user-guide/custom-themes/#template-variables
[mkdocs-block]: https://www.mkdocs.org/user-guide/styling-your-docs/#overriding-template-blocks
