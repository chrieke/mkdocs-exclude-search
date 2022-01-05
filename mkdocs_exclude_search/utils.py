from typing import List


def iterate_all_values(nested_dict: dict):
    """
    Returns an iterator that returns all values of a (nested) iterable of the form
    {'a': ['aa', {'b': ['cc', {'d': ['ee', 'ff', {'d': ['gg', 'hh']}]}]}]}

    Inspired by https://gist.github.com/PatrikHlobil/9d045e43fe44df2d5fd8b570f9fd78cc
    """
    if isinstance(nested_dict, dict):
        for value in nested_dict.values():
            if not isinstance(value, (dict, list)):
                yield value
            for ret in iterate_all_values(value):
                yield ret
    elif isinstance(nested_dict, list):
        for el in nested_dict:
            for ret in iterate_all_values(el):
                yield ret
    elif isinstance(nested_dict, str):
        yield nested_dict


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

    navigation_paths = [nav_path.replace(".md", "/") for nav_path in navigation_paths]

    return navigation_paths
