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

- List the markdown files to be excluded under `exclude` using the format `filename.md`. Don't provide the directory of the file!
- Exclude specific heading subsections using the format `filename.md#some-heading`. Chapter names are all lowercase, `-` as separator, no spaces.
- Exclude all markdown files within a directory with `dirname/*.md` or `dirname/dirname2/*.md`.
- To only include a specific heading subsection of an excluded file, list the subsection under `ignore`. 

```yaml
plugins:
  - search
  - exclude-search:
      exclude:
        - second.md  # Do not provide the directory of the file, only the filename!
        - third.md#some-heading  
        - dir/*.md  # Only to exclude all files within a directory provide the directory!
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
- all markdown files within `dir` and `dir2/sub`.



## See Also

More information about templates [here][mkdocs-template].

More information about blocks [here][mkdocs-block].

[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[mkdocs-template]: https://www.mkdocs.org/user-guide/custom-themes/#template-variables
[mkdocs-block]: https://www.mkdocs.org/user-guide/styling-your-docs/#overriding-template-blocks
