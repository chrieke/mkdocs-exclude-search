from pathlib import Path
import json

import pytest

from mkdocs_exclude_search.plugin import ExcludeSearch


CONFIG = {"plugins": ["search"]}
TO_EXCLUDE = [
    "chapter_exclude_all/*",
    "chapter_exclude_heading2/*#single-header-chapter_exclude_heading2-bbex",
    "dir_chapter_ignore_heading3.md",
    "all_dir/*.md#alldir-header-all_dir_ignore_heading1-aain",
    "all_dir_sub/all_dir_sub2/*.md",
]

RESOLVED_EXCLUDED_RECORDS = [
    ("chapter_exclude_all.md", None),
    ("chapter_exclude_heading2.md", "single-header-chapter_exclude_heading2-bbex"),
    ("dir_chapter_exclude_all.md", None),
    ("dir_chapter_ignore_heading3.md", None),
    ("all_dir/*.md", None),
    ("all_dir_sub/all_dir_sub2/*.md", None),
]

TO_IGNORE = [
    "dir_chapter_ignore_heading3.md#dir-single-header-dir_chapter_ignore_heading3-ccin",
    "all_dir_ignore_heading1.md#alldir-header-all_dir_ignore_heading1-aain",
]

RESOLVED_IGNORED_CHAPTERS = [
    (
        "dir_chapter_ignore_heading3.md",
        "dir-single-header-dir_chapter_ignore_heading3-ccin",
    ),
    ("all_dir_ignore_heading1.md", "alldir-header-all_dir_ignore_heading1-aain"),
    ("dir_chapter_ignore_heading3.md", None),
    ("all_dir_ignore_heading1.md", None),
]

EXCLUDE_TAGS = False

INCLUDED_RECORDS = [
    {"location": "index.html", "text": "Index Hello, hello", "title": "index"},
    {"location": "index.html#index", "text": "Hello, hello", "title": "Index"},
    {
      "location": "chapter_exclude_heading2/index.html",
      "text": "single chapter_exclude_heading2 Header Ain single header chapter_exclude_heading2 AAin single text chapter_exclude_heading2 AAin single header chapter_exclude_heading2 BBex single text chapter_exclude_heading2 BBex",
      "title": "chapter_exclude_heading2"
    },
    {
      "location": "chapter_exclude_heading2/index.html#single-chapter_exclude_heading2-header-ain",
      "text": "",
      "title": "single chapter_exclude_heading2 Header Ain"
    },
    {
      "location": "chapter_exclude_heading2/index.html#single-header-chapter_exclude_heading2-aain",
      "text": "single text chapter_exclude_heading2 AAin",
      "title": "single header chapter_exclude_heading2 AAin"
    },
    
    {
      "location": "all_dir/all_dir/index.html",
      "text": "alldir Header all_dir Aex alldir header all_dir AAex alldir text all_dir AAex alldir header all_dir BBex alldir text all_dir BBex",
      "title": "all_dir"
    },
    {
      "location": "all_dir/all_dir/index.html#alldir-header-all_dir-aex",
      "text": "",
      "title": "alldir Header all_dir Aex"
    },
    {
      "location": "all_dir/all_dir/index.html#alldir-header-all_dir-aaex",
      "text": "alldir text all_dir AAex",
      "title": "alldir header all_dir AAex"
    },
    {
      "location": "all_dir/all_dir/index.html#alldir-header-all_dir-bbex",
      "text": "alldir text all_dir BBex",
      "title": "alldir header all_dir BBex"
    },
    {
      "location": "all_dir/all_dir_ignore_heading1/index.html",
      "text": "alldir Header all_dir_ignore_heading1 Aex alldir header all_dir_ignore_heading1 AAin alldir text all_dir_ignore_heading1 AAin alldir header all_dir_ignore_heading1 BBex alldir text all_dir_ignore_heading1 BBex",
      "title": "all_dir_ignore_heading1"
    },
    {
      "location": "all_dir/all_dir_ignore_heading1/index.html#alldir-header-all_dir_ignore_heading1-aex",
      "text": "",
      "title": "alldir Header all_dir_ignore_heading1 Aex"
    },
    {
      "location": "all_dir/all_dir_ignore_heading1/index.html#alldir-header-all_dir_ignore_heading1-bbex",
      "text": "alldir text all_dir_ignore_heading1 BBex",
      "title": "alldir header all_dir_ignore_heading1 BBex"
    },
    {
      "location": "dir/dir_chapter_ignore_heading3/",
      "text": "dir single Header dir_chapter_ignore_heading3 Aex dir single header dir_chapter_ignore_heading3 AAex dir single text dir_chapter_ignore_heading3 AAex dir single header dir_chapter_ignore_heading3 CCin dir single text dir_chapter_ignore_heading3 CCin",
      "title": "dir_chapter_ignore_heading3"
    },
    {
      "location": "dir/dir_chapter_ignore_heading3/#dir-single-header-dir_chapter_ignore_heading3-aex",
      "text": "",
      "title": "dir single Header dir_chapter_ignore_heading3 Aex"
    },
    {
      "location": "dir/dir_chapter_ignore_heading3/#dir-single-header-dir_chapter_ignore_heading3-aaex",
      "text": "dir single text dir_chapter_ignore_heading3 AAex",
      "title": "dir single header dir_chapter_ignore_heading3 AAex"
    },
    {
      "location": "dir/dir_chapter_ignore_heading3/#dir-single-header-dir_chapter_ignore_heading3-ccin",
      "text": "dir single text dir_chapter_ignore_heading3 CCin",
      "title": "dir single header dir_chapter_ignore_heading3 CCin"
    },
    {
        "location": "tags.html",
        "text": "Contents grouped by tag testing Welcome unimportant Welcome",
        "title": "Tags",
    },
    {
        "location": "tags.html#contents-grouped-by-tag",
        "text": "",
        "title": "Contents grouped by tag",
    },
    {"location": "tags.html#testing", "text": "Welcome", "title": "testing"},
    {"location": "tags.html#unimportant", "text": "Welcome", "title": "unimportant"},
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


def test_resolve_excluded_records():
    resolved_excluded_records = ExcludeSearch.resolve_excluded_records(
        to_exclude=TO_EXCLUDE
    )
    assert resolved_excluded_records == RESOLVED_EXCLUDED_RECORDS


def test_resolve_ignored_chapters():
    resolved_ignored_chapters = ExcludeSearch.resolve_ignored_chapters(
        to_ignore=TO_IGNORE
    )
    assert resolved_ignored_chapters == RESOLVED_IGNORED_CHAPTERS


def test_select_records():
    _location_ = Path(__file__).resolve().parent
    with open(_location_.joinpath("mock_data/mock_search_index.json"), "r") as f:
        mock_search_index = json.load(f)

    included_records = ExcludeSearch.select_included_records(
        search_index=mock_search_index,
        to_exclude=RESOLVED_EXCLUDED_RECORDS,
        to_ignore=RESOLVED_IGNORED_CHAPTERS,
        exclude_tags=EXCLUDE_TAGS,
    )
    assert isinstance(included_records, list)
    assert included_records == INCLUDED_RECORDS


def test_select_records_exclude_tags():
    _location_ = Path(__file__).resolve().parent
    with open(_location_.joinpath("mock_data/mock_search_index.json"), "r") as f:
        mock_search_index = json.load(f)

    included_records = ExcludeSearch.select_included_records(
        search_index=mock_search_index,
        to_exclude=RESOLVED_EXCLUDED_RECORDS,
        to_ignore=RESOLVED_IGNORED_CHAPTERS,
        exclude_tags=True,
    )

    included_records_without_tags = [
        rec for rec in INCLUDED_RECORDS if not "tags.html" in rec["location"]
    ]
    assert isinstance(included_records_without_tags, list)
    assert included_records == included_records_without_tags
