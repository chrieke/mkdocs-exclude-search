"""Tests for the plugin module."""

import sys

import pytest
from mkdocs.commands.build import build
from mkdocs.config.base import load_config

from src.plugin import ExcludeSearch


CONFIG = {"plugins": ["search"]}
TO_EXCLUDE = ["abc"]
EXCLUDE_TAGS = False


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
