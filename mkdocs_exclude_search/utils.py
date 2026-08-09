from typing import List, Optional, Tuple


def iterate_all_values(nested_dict: dict):
    """
    Returns an iterator that returns all values of a (nested) iterable of the form
    {'a': ['aa', {'b': ['cc', {'d': ['ee', 'ff', {'d': ['gg', 'hh']}]}]}]}

    Inspired by https://gist.github.com/PatrikHlobil/9d045e43fe44df2d5fd8b570f9fd78cc
    """
    if isinstance(nested_dict, dict):
        for value in nested_dict.values():
            yield from iterate_all_values(value)
    elif isinstance(nested_dict, list):
        for el in nested_dict:
            yield from iterate_all_values(el)
    elif isinstance(nested_dict, str):
        yield nested_dict


def split_header(entry: str) -> Tuple[str, Optional[str]]:
    """
    Split an entry or record location into file and header part, e.g.
    'dir/chapter.md#some-header' -> ('dir/chapter.md', 'some-header').

    Only the first `#` separates the two, any further `#` belongs to the header name.
    """
    file_name, _, header_name = entry.partition("#")
    return file_name, header_name or None


def strip_md_suffix(file_name: str) -> str:
    """'dir/chapter.md' -> 'dir/chapter'"""
    if file_name.endswith(".md"):
        return file_name[: -len(".md")]
    return file_name


def strip_url_suffix(rec_file_name: str) -> str:
    """
    Strip the url suffix of a search index record location, so that it can be compared
    with a user provided entry. Depending on the mkdocs `use_directory_urls` setting,
    a page is located at 'dir/chapter/' or at 'dir/chapter.html'.
    """
    if rec_file_name.endswith("/"):
        return rec_file_name[:-1]
    if rec_file_name.endswith(".html"):
        return rec_file_name[: -len(".html")]
    return rec_file_name


def explode_navigation(navigation: list) -> List[str]:
    # Paths to chapters in mkdocs.yml navigation section to compare
    # with unreferenced files.
    navigation_paths = []

    for chapter in navigation:
        if isinstance(chapter, str):
            # e.g. - index.md   (without name in nav)
            navigation_paths.append(chapter)
        elif isinstance(chapter, dict):
            chapter_paths = list(chapter.values())[0]
            if isinstance(chapter_paths, str):
                # e.g. - chapter_exclude_all: chapter_exclude_all.md
                navigation_paths.append(chapter_paths)
            elif isinstance(chapter_paths, list):
                # e.g. - toplvl_chapter:
                #         - toplvl_chapter/file_in_toplvl_chapter.md
                exploded_chapter_paths = iterate_all_values(nested_dict=chapter)
                navigation_paths.extend(exploded_chapter_paths)

    return [strip_md_suffix(nav_path) for nav_path in navigation_paths]
