"""Tests for the plugin module."""

import sys

import pytest
from mkdocs.commands.build import build
from mkdocs.config.base import load_config

from mkdocs_exclude_search.plugin import ExcludeSearch


CONFIG = {"plugins": ["search"]}
TO_EXCLUDE = ["abc"]
EXCLUDE_TAGS = False

TO_IGNORE = [
    "dir_chapter_ignore_heading3.md#dir-single-header-dir_chapter_ignore_heading3-ccin",
    "all_dir_ignore_heading1.md#alldir-header-all_dir_ignore_heading1-aain",
]


def test_check_config():
    ExcludeSearch.check_config(
        config=CONFIG, to_exclude=TO_EXCLUDE, exclude_tags=EXCLUDE_TAGS
    )
    ExcludeSearch.check_config(config=CONFIG, to_exclude=TO_EXCLUDE, exclude_tags=True)
    ExcludeSearch.check_config(config=CONFIG, to_exclude=[], exclude_tags=True)


def test_check_config_raises_search_deactivated():
    with pytest.raises(ValueError):
        ExcludeSearch.check_config(
            config={"plugins": ["abc"]},
            to_exclude=TO_EXCLUDE,
            exclude_tags=EXCLUDE_TAGS,
        )


def test_check_config_raises_no_exclusion():
    with pytest.raises(ValueError):
        ExcludeSearch.check_config(
            config=CONFIG, to_exclude=[], exclude_tags=EXCLUDE_TAGS
        )


def test_resolve_ignored_chapters():
    resolved_ignored_chapters = ExcludeSearch.resolve_ignored_chapters(
        to_ignore=TO_IGNORE
    )
    assert resolved_ignored_chapters == [
        "dir_chapter_ignore_heading3#dir-single-header-dir_chapter_ignore_heading3-ccin",
        "all_dir_ignore_heading1#alldir-header-all_dir_ignore_heading1-aain",
        "dir_chapter_ignore_heading3",
        "all_dir_ignore_heading1",
    ]
