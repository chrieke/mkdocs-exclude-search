from pathlib import Path
import json

import pytest

from mkdocs_exclude_search.plugin import ExcludeSearch


CONFIG = {"plugins": ["search"]}
TO_EXCLUDE = [
    "chapter_exclude_all.md",
    "chapter_exclude_heading2.md#single-header-chapter_exclude_heading2-bbex",
    "dir_chapter_exclude_all.md",
    "dir_chapter_ignore_heading3.md",
    "all_dir/*.md",
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
    {"location": "", "text": "Index Hello, hello", "title": "index"},
    {"location": "#index", "text": "Hello, hello", "title": "Index"},
    {
        "location": "chapter_exclude_heading2/",
        "text": "single chapter_exclude_heading2 Header Ain single header chapter_exclude_heading2 AAin single text chapter_exclude_heading2 AAin single header chapter_exclude_heading2 BBex single text chapter_exclude_heading2 BBex",
        "title": "chapter_exclude_heading2",
    },
    {
        "location": "chapter_exclude_heading2/#single-chapter_exclude_heading2-header-ain",
        "text": "",
        "title": "single chapter_exclude_heading2 Header Ain",
    },
    {
        "location": "chapter_exclude_heading2/#single-header-chapter_exclude_heading2-aain",
        "text": "single text chapter_exclude_heading2 AAin",
        "title": "single header chapter_exclude_heading2 AAin",
    },
    {
        "location": "all_dir/all_dir_ignore_heading1/",
        "text": "alldir Header all_dir_ignore_heading1 Aex alldir header all_dir_ignore_heading1 AAin alldir text all_dir_ignore_heading1 AAin alldir header all_dir_ignore_heading1 BBex alldir text all_dir_ignore_heading1 BBex",
        "title": "all_dir_ignore_heading1",
    },
    {
        "location": "all_dir/all_dir_ignore_heading1/#alldir-header-all_dir_ignore_heading1-aain",
        "text": "alldir text all_dir_ignore_heading1 AAin",
        "title": "alldir header all_dir_ignore_heading1 AAin",
    },
    {
        "location": "dir/dir_chapter_ignore_heading3/",
        "text": "dir single Header dir_chapter_ignore_heading3 Aex dir single header dir_chapter_ignore_heading3 AAex dir single text dir_chapter_ignore_heading3 AAex dir single header dir_chapter_ignore_heading3 CCin dir single text dir_chapter_ignore_heading3 CCin",
        "title": "dir_chapter_ignore_heading3",
    },
    {
        "location": "dir/dir_chapter_ignore_heading3/#dir-single-header-dir_chapter_ignore_heading3-ccin",
        "text": "dir single text dir_chapter_ignore_heading3 CCin",
        "title": "dir single header dir_chapter_ignore_heading3 CCin",
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
    assert isinstance(resolved_excluded_records, list)
    assert isinstance(resolved_excluded_records[0], tuple)
    assert resolved_excluded_records == RESOLVED_EXCLUDED_RECORDS


def test_resolve_ignored_chapters():
    resolved_ignored_chapters = ExcludeSearch.resolve_ignored_chapters(
        to_ignore=TO_IGNORE
    )
    assert isinstance(resolved_ignored_chapters, list)
    assert isinstance(resolved_ignored_chapters[0], tuple)
    assert resolved_ignored_chapters == RESOLVED_IGNORED_CHAPTERS


def test_is_tag_record():
    assert ExcludeSearch.is_tag_record("tags.html")
    assert ExcludeSearch.is_tag_record("tags.html#abc")


def test_is_root_record():
    assert ExcludeSearch.is_root_record("")
    assert ExcludeSearch.is_root_record("index.html")


def test_is_ignored_record():
    assert ExcludeSearch.is_ignored_record(
        rec_file_name="all_dir/all_dir_ignore_heading1/",
        rec_header_name=None,
        to_ignore=[("all_dir_ignore_heading1.md", None)],
    )
    assert ExcludeSearch.is_ignored_record(
        rec_file_name="all_dir/all_dir_ignore_heading1/",
        rec_header_name="alldir-header-all_dir_ignore_heading1-aain",
        to_ignore=[
            ("all_dir_ignore_heading1.md", "alldir-header-all_dir_ignore_heading1-aain")
        ],
    )

    assert not ExcludeSearch.is_ignored_record(
        rec_file_name="all_dir/all_dir_ignore_heading1/",
        rec_header_name="alldir-header-all_dir_ignore_heading1-aain",
        to_ignore=[("all_dir_ignore_heading1.md", None)],
    )
    assert not ExcludeSearch.is_ignored_record(
        rec_file_name="all_dir/a/", rec_header_name="b", to_ignore=[("c.md", "b")]
    )



def test_is_excluded_record():
    # file
    assert ExcludeSearch.is_excluded_record(
        rec_file_name="chapter_exclude_all/",
        rec_header_name=None,
        to_exclude=[("chapter_exclude_all.md", None)],
    )
    # file with multiple excluded
    assert not ExcludeSearch.is_excluded_record(
        rec_file_name="chapter_exclude_all/",
        rec_header_name=None,
        to_exclude=[("chapter_exclude_all.md", "something.md")],
    )
    # file + header
    assert ExcludeSearch.is_excluded_record(
        rec_file_name="chapter_exclude_all/",
        rec_header_name="header-chapter_exclude_all-aex",
        to_exclude=[("chapter_exclude_all.md", None)],
    )
    # dir
    assert ExcludeSearch.is_excluded_record(
        rec_file_name="all_dir/some-chapter/",
        rec_header_name=None,
        to_exclude=[("all_dir/*.md", None)],
    )
    # dir + header
    assert ExcludeSearch.is_excluded_record(
        rec_file_name="all_dir/some-chapter/",
        rec_header_name="all_dir/some-chapter-aex",
        to_exclude=[("all_dir/*.md", None)],
    )
    # subdir
    assert ExcludeSearch.is_excluded_record(
        rec_file_name="all_dir_sub/all_dir_sub2/some-chapter/",
        rec_header_name=None,
        to_exclude=[("all_dir_sub/all_dir_sub2/*.md", None)],
    )
    #subdir + header
    assert ExcludeSearch.is_excluded_record(
        rec_file_name="all_dir_sub/all_dir_sub2/some-chapter/",
        rec_header_name="alldir-header-all_dir_sub2-aex",
        to_exclude=[("all_dir_sub/all_dir_sub2/*.md", None)],
    )


def test_is_excluded_record_ignores_partial_filename_matches():
    assert not ExcludeSearch.is_excluded_record(
        rec_file_name="do_not_match_chapter_exclude_all/",
        rec_header_name=None,
        to_exclude=[("chapter_exclude_all.md", None)],
    )


def test_select_records():
    _location_ = Path(__file__).resolve().parent
    with open(_location_.joinpath("mock_data/mock_search_index.json"), "r") as f:
        mock_search_index = json.load(f)

    included_records = ExcludeSearch().select_included_records(
        search_index=mock_search_index,
        to_exclude=RESOLVED_EXCLUDED_RECORDS,
        to_ignore=RESOLVED_IGNORED_CHAPTERS,
        exclude_tags=EXCLUDE_TAGS,
    )
    assert isinstance(included_records, list)
    assert isinstance(included_records[0], dict)
    assert included_records == INCLUDED_RECORDS


def test_select_records_exclude_tags():
    _location_ = Path(__file__).resolve().parent
    with open(_location_.joinpath("mock_data/mock_search_index.json"), "r") as f:
        mock_search_index = json.load(f)

    included_records = ExcludeSearch().select_included_records(
        search_index=mock_search_index,
        to_exclude=RESOLVED_EXCLUDED_RECORDS,
        to_ignore=RESOLVED_IGNORED_CHAPTERS,
        exclude_tags=True,
    )
    assert len(included_records) != len(INCLUDED_RECORDS)
    for rec in included_records:
        assert not "tags.html" in rec["location"]
