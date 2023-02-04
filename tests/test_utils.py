from .globals import NAVIGATION
from .context import iterate_all_values, explode_navigation


def test_iterate_all_values():
    nav = {"a": ["aa", {"b": ["cc", {"d": ["ee", "ff", {"d": ["gg", "hh"]}]}]}]}

    nav_paths = list(iterate_all_values(nested_dict=nav))
    assert isinstance(nav_paths, list)
    assert nav_paths == ["aa", "cc", "ee", "ff", "gg", "hh"]


def test_explode_navigation():
    nav_paths = explode_navigation(navigation=NAVIGATION)
    assert isinstance(nav_paths, list)
    assert nav_paths == [
        "index/",
        "without_nav_name/",
        "chapter_exclude_all/",
        "toplvl_chapter/file_in_toplvl_chapter/",
        "toplvl_chapter/sub_chapter/file1_in_sub_chapter/",
        "toplvl_chapter/sub_chapter/file2_in_sub_chapter/",
    ]
