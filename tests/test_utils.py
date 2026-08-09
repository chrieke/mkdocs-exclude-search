from .globals import NAVIGATION
from .context import (
    iterate_all_values,
    explode_navigation,
    split_header,
    strip_md_suffix,
    strip_url_suffix,
)


def test_iterate_all_values():
    nav = {"a": ["aa", {"b": ["cc", {"d": ["ee", "ff", {"d": ["gg", "hh"]}]}]}]}

    nav_paths = list(iterate_all_values(nested_dict=nav))
    assert isinstance(nav_paths, list)
    assert nav_paths == ["aa", "cc", "ee", "ff", "gg", "hh"]


def test_iterate_all_values_named_entry_yielded_once():
    # named chapter entries are dict values, they must not be yielded twice
    nav = {"toplvl_chapter": [{"named": "a.md"}, "b.md"]}

    assert list(iterate_all_values(nested_dict=nav)) == ["a.md", "b.md"]


def test_explode_navigation_named_subchapter():
    # e.g. - toplvl_chapter:
    #         - named: toplvl_chapter/a.md
    navigation = [{"toplvl_chapter": [{"named": "toplvl_chapter/a.md"}]}]

    assert explode_navigation(navigation=navigation) == ["toplvl_chapter/a"]


def test_split_header():
    assert split_header("dir/chapter.md") == ("dir/chapter.md", None)
    assert split_header("dir/chapter.md#header") == ("dir/chapter.md", "header")
    # only the first `#` separates, mkdocs anchors may contain further ones
    assert split_header("dir/chapter.md#header#sub") == ("dir/chapter.md", "header#sub")


def test_strip_md_suffix():
    assert strip_md_suffix("dir/chapter.md") == "dir/chapter"
    assert strip_md_suffix("dir/*") == "dir/*"
    # only the suffix is stripped, not an occurrence within the path
    assert strip_md_suffix("dir.md_files/chapter.md") == "dir.md_files/chapter"


def test_strip_url_suffix():
    # use_directory_urls: true (default)
    assert strip_url_suffix("dir/chapter/") == "dir/chapter"
    # use_directory_urls: false
    assert strip_url_suffix("dir/chapter.html") == "dir/chapter"
    assert strip_url_suffix("") == ""


def test_explode_navigation():
    nav_paths = explode_navigation(navigation=NAVIGATION)
    assert isinstance(nav_paths, list)
    assert nav_paths == [
        "index",
        "without_nav_name",
        "chapter_exclude_all",
        "toplvl_chapter/file_in_toplvl_chapter",
        "toplvl_chapter/sub_chapter/file1_in_sub_chapter",
        "toplvl_chapter/sub_chapter/file2_in_sub_chapter",
    ]
