from pathlib import Path
import json

import pytest

from .context import ExcludeSearch
from .globals import (
    TO_EXCLUDE,
    RESOLVED_EXCLUDED_RECORDS,
    TO_IGNORE,
    RESOLVED_IGNORED_CHAPTERS,
    EXCLUDE_UNREFERENCED,
    EXCLUDE_TAGS,
    INCLUDED_RECORDS,
)


@pytest.mark.parametrize(
    "exclude,exclude_unreferenced,exclude_tags",
    [
        (TO_EXCLUDE, EXCLUDE_UNREFERENCED, EXCLUDE_TAGS),
        (TO_EXCLUDE, True, True),
        ([], True, EXCLUDE_TAGS),
        ([], EXCLUDE_UNREFERENCED, True),
        ([], True, True),
    ],
)
def test_check_config(exclude, exclude_unreferenced, exclude_tags):
    ex = ExcludeSearch()
    ex.config = dict(
        {
            "exclude": exclude,
            "exclude_unreferenced": exclude_unreferenced,
            "exclude_tags": exclude_tags,
        }
    )
    ex.check_config(plugins=["search"])


def test_check_config_raises_search_deactivated():
    ex = ExcludeSearch()
    with pytest.raises(ValueError):
        ex.check_config(plugins=["abc"])


def test_check_config_raises_no_exclusion():
    ex = ExcludeSearch()
    ex.config = dict(
        {
            "exclude": [],
            "exclude_unreferenced": EXCLUDE_UNREFERENCED,
            "exclude_tags": EXCLUDE_TAGS,
        }
    )
    with pytest.raises(ValueError):
        ex.check_config(plugins=["search"])


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
    assert set(resolved_ignored_chapters) == set(RESOLVED_IGNORED_CHAPTERS)


def test_is_tag_record():
    assert ExcludeSearch.is_tag_record("tags.html")
    assert ExcludeSearch.is_tag_record("tags.html#abc")


def test_is_root_record():
    assert ExcludeSearch.is_root_record("")
    assert ExcludeSearch.is_root_record("index.html")


def test_is_ignored_record():
    assert ExcludeSearch.is_ignored_record(
        rec_file_name="all_dir/all_dir_ignore_heading1/",
        rec_header_name="alldir-header-all_dir_ignore_heading1-aain",
        to_ignore=[
            (
                "all_dir/all_dir_ignore_heading1.md",
                "alldir-header-all_dir_ignore_heading1-aain",
            )
        ],
    )


def test_is_not_ignored_record():
    # wrong dir specified
    assert not ExcludeSearch.is_ignored_record(
        rec_file_name="all_dir/all_dir_ignore_heading1/",
        rec_header_name="alldir-header-all_dir_ignore_heading1-aain",
        to_ignore=[
            ("all_dir_ignore_heading1.md", "alldir-header-all_dir_ignore_heading1-aain")
        ],
    )
    # no heading specified
    assert not ExcludeSearch.is_ignored_record(
        rec_file_name="all_dir/all_dir_ignore_heading1/",
        rec_header_name="alldir-header-all_dir_ignore_heading1-aain",
        to_ignore=[("all_dir/all_dir_ignore_heading1.md", None)],
    )
    # different files
    assert not ExcludeSearch.is_ignored_record(
        rec_file_name="a.md", rec_header_name="b", to_ignore=[("c.md", "b")]
    )


def test_is_excluded_record_file():
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
    # file + header (not specifically excluded)
    assert ExcludeSearch.is_excluded_record(
        rec_file_name="chapter_exclude_all/",
        rec_header_name="header-chapter_exclude_all-aex",
        to_exclude=[("chapter_exclude_all.md", None)],
    )
    # file + header (specifically excluded)
    assert ExcludeSearch.is_excluded_record(
        rec_file_name="chapter_exclude_all/",
        rec_header_name="header-chapter_exclude_all-aex",
        to_exclude=[("chapter_exclude_all.md", "header-chapter_exclude_all-aex")],
    )
    # file in dir
    assert ExcludeSearch.is_excluded_record(
        rec_file_name="dir/dir_chapter_exclude_all/",
        rec_header_name=None,
        to_exclude=[("dir/dir_chapter_exclude_all.md", None)],
    )


def test_is_excluded_record_dir():
    # all dir
    assert ExcludeSearch.is_excluded_record(
        rec_file_name="all_dir/some-chapter/",
        rec_header_name=None,
        to_exclude=[("all_dir/*", None)],
    )
    assert ExcludeSearch.is_excluded_record(
        rec_file_name="all_dir/some-chapter/",
        rec_header_name=None,
        to_exclude=[("all_dir/*", None)],
    )
    # all dir + header
    assert ExcludeSearch.is_excluded_record(
        rec_file_name="all_dir/some-chapter/",
        rec_header_name="all_dir/some-chapter-aex",
        to_exclude=[("all_dir/*", None)],
    )
    # all subdir
    assert ExcludeSearch.is_excluded_record(
        rec_file_name="all_dir_sub/all_dir_sub2/some-chapter/",
        rec_header_name=None,
        to_exclude=[("all_dir_sub/all_dir_sub2/*", None)],
    )
    # all subdir + header
    assert ExcludeSearch.is_excluded_record(
        rec_file_name="all_dir_sub/all_dir_sub2/some-chapter/",
        rec_header_name="alldir-header-all_dir_sub2-aex",
        to_exclude=[("all_dir_sub/all_dir_sub2/*", None)],
    )


def test_is_excluded_record_wildcard():
    # file within subdir wildcard
    assert ExcludeSearch.is_excluded_record(
        rec_file_name="all_dir_sub/all_dir_sub2/all_dir_sub2_1/",
        rec_header_name=None,
        to_exclude=[("all_dir_sub/*/all_dir_sub2_1.md", None)],
    )
    # file within multiple subdir wildcard
    assert ExcludeSearch.is_excluded_record(
        rec_file_name="all_dir_sub/all_dir_sub2/all_dir_sub2_again/all_dir_sub2_1/",
        rec_header_name=None,
        to_exclude=[("all_dir_sub/*/all_dir_sub2_1.md", None)],
    )
    # file within multiple subdir wildcard + header
    assert ExcludeSearch.is_excluded_record(
        rec_file_name="all_dir_sub/all_dir_sub2/all_dir_sub2_again/all_dir_sub2_1/",
        rec_header_name="alldir-header-all_dir_sub2-aex",
        to_exclude=[
            ("all_dir_sub/*/all_dir_sub2_1.md", "alldir-header-all_dir_sub2-aex")
        ],
    )


def test_is_unreferenced_record_unreferenced():
    # unreferenced file, not listed in mkdocs.yml nav
    assert ExcludeSearch.is_unreferenced_record(
        rec_file_name="unreferenced/",
        navigation_items=["index/", "chapter_exclude_all/"],
    )

    assert not ExcludeSearch.is_unreferenced_record(
        rec_file_name="chapter_exclude_all/",
        navigation_items=["index/", "chapter_exclude_all/"],
    )


def test_is_not_excluded_record():
    # file in dir without dir specified
    assert not ExcludeSearch.is_excluded_record(
        rec_file_name="dir/dir_chapter_exclude_all/",
        rec_header_name=None,
        to_exclude=[("dir_chapter_exclude_all.md", None)],
    )
    # partial filename matches
    assert not ExcludeSearch.is_excluded_record(
        rec_file_name="do_not_match_chapter_exclude_all/",
        rec_header_name=None,
        to_exclude=[("chapter_exclude_all.md", None)],
    )
    # partial path match
    assert not ExcludeSearch.is_excluded_record(
        rec_file_name="all_dir_sub/",
        rec_header_name=None,
        to_exclude=[("all_dir_sub/*/all_dir_sub2_1.md", None)],
    )


def test_select_records():
    _location_ = Path(__file__).resolve().parent
    with open(_location_.joinpath("mock_data/mock_search_index.json"), "r") as f:
        mock_search_index = json.load(f)

    included_records = ExcludeSearch().select_included_records(
        search_index=mock_search_index,
        to_exclude=RESOLVED_EXCLUDED_RECORDS,
        to_ignore=RESOLVED_IGNORED_CHAPTERS,
        navigation_items=[],
        exclude_tags=EXCLUDE_TAGS,
    )
    assert isinstance(included_records, list)
    assert isinstance(included_records[0], dict)
    assert included_records == INCLUDED_RECORDS


def test_select_records_unreferenced():
    _location_ = Path(__file__).resolve().parent
    with open(_location_.joinpath("mock_data/mock_search_index.json"), "r") as f:
        mock_search_index = json.load(f)

    included_records = ExcludeSearch().select_included_records(
        search_index=mock_search_index,
        to_exclude=[],
        to_ignore=[],
        navigation_items=["chapter_exclude_all/"],
        exclude_unreferenced=True,
    )
    assert isinstance(included_records, list)
    assert isinstance(included_records[0], dict)
    assert included_records != INCLUDED_RECORDS
    assert len(included_records) == 10


def test_select_records_exclude_tags():
    _location_ = Path(__file__).resolve().parent
    with open(_location_.joinpath("mock_data/mock_search_index.json"), "r") as f:
        mock_search_index = json.load(f)

    included_records = ExcludeSearch().select_included_records(
        search_index=mock_search_index,
        to_exclude=RESOLVED_EXCLUDED_RECORDS,
        to_ignore=RESOLVED_IGNORED_CHAPTERS,
        navigation_items=[],
        exclude_tags=True,
    )
    assert len(included_records) != len(INCLUDED_RECORDS)
    for rec in included_records:
        assert not "tags.html" in rec["location"]
