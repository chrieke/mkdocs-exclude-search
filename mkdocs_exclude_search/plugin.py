import json
import logging
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Union

import mkdocs
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from packaging.version import Version

from mkdocs_exclude_search.utils import (
    explode_navigation,
    split_header,
    strip_md_suffix,
    strip_url_suffix,
)


def get_logger():
    logger = logging.getLogger("mkdocs.plugins.mkdocs-exclude-search")
    MKDOCS_LOG_VERSION = "1.2"
    if Version(mkdocs.__version__) < Version(MKDOCS_LOG_VERSION):
        # filter doesn't do anything since that version
        # pylint: disable=import-outside-toplevel, no-name-in-module
        from mkdocs.utils import warning_filter

        logger.addFilter(warning_filter)

    return logger


logger = get_logger()


class ExcludeSearch(BasePlugin):
    """
    Excludes selected files, nav chapters and headers from the search index.
    """

    config_scheme = (
        ("exclude", config_options.Type((str, list), default=[])),
        ("ignore", config_options.Type((str, list), default=[])),
        ("exclude_unreferenced", config_options.Type(bool, default=False)),
        ("exclude_tags", config_options.Type(bool, default=False)),
    )

    def validate_config(self, plugins: list[str]):
        """
        Validate and normalize the mkdocs-exclude-search plugin configuration.
        """
        # `exclude` and `ignore` may be a single string, everything below expects a list.
        for option in ("exclude", "ignore"):
            if isinstance(self.config.get(option), str):
                self.config[option] = [self.config[option]]

        if not ("search" in plugins or "material/search" in plugins):
            message = (
                "mkdocs-exclude-search plugin is activated but has no effect as "
                "search plugin is deactivated!"
            )
            logger.debug(message)
            raise ValueError(message)

        if (
            not self.config["exclude"]
            and not self.config["exclude_unreferenced"]
            and not self.config["exclude_tags"]
        ):
            message = (
                "No excluded search entries selected for mkdocs-exclude-search, "
                "the plugin has no effect!"
            )
            logger.info(message)
            raise ValueError(message)

        invalid_ignored = [x for x in self.config.get("ignore", []) if "#" not in x]
        if invalid_ignored:
            message = (
                f"mkdocs-exclude-search configuration for `ignore` can only be "
                f"headers (containing `#`), the following entries will be ignored: {invalid_ignored}"
            )
            logger.info(message)
            self.config["ignore"] = [
                x for x in self.config["ignore"] if x not in invalid_ignored
            ]

    @staticmethod
    def resolve_excluded_records(
        to_exclude: list[str],
    ) -> list:
        """
        Resolve the search index file-name and header-names from the user provided excluded entries.

        Args:
            to_exclude: The user provided list of excluded entries for files,
                headers and directories ("*").

        Returns:
            A list with each resolved entry as a tuple of (file-name, header-name/None).
        """
        # TODO: This currently could exclude files with an excluded folder of the same name.
        return [split_header(entry) for entry in to_exclude]

    @staticmethod
    def resolve_ignored_chapters(to_ignore: list[str]) -> list:
        """
        Supplement the search index main entry for each user provided ignored header.

        In order for a header subchapter to be available in the search index, it requires one
        "file-name" entry and one "file-name/header-name" entry.

        Args:
            to_ignore: The user provided list of ignored entries for chapters.

        Returns:
            A list with each resolved entry as a tuple of (file-name, header-name/None),
            and with the supplemented main_name entries.
        """
        file_name_entries = []
        file_header_names_entries = []
        for entry in to_ignore:
            file_name, header_name = split_header(entry)
            file_name_entries.append((file_name, None))
            file_header_names_entries.append((file_name, header_name))

        ignored_chapters = file_name_entries + file_header_names_entries  # type: ignore
        return ignored_chapters

    @staticmethod
    def is_unreferenced_record(rec_file_name: str, navigation_items: list[str]) -> bool:
        """
        Unreferenced markdown files that are not contained in mkdocs.yml navigation
        nav section. navigation_items are suffix-free, as returned by explode_navigation.
        """
        return strip_url_suffix(rec_file_name) not in navigation_items

    @staticmethod
    def is_tag_record(rec_file_name: str) -> bool:
        """Tags entries of mkdocs-plugin-tags.

        The tags page is located at 'tags/' with the default `use_directory_urls`,
        'tags.html' without.
        """
        stripped = strip_url_suffix(rec_file_name)
        return stripped == "tags" or stripped.endswith("/tags")

    @staticmethod
    def is_root_record(rec_file_name: str) -> bool:
        """Required mkdocs root file, i.e. the site index page.

        Its location is "" with the default `use_directory_urls`, "index.html" without.
        """
        return rec_file_name in ("", "index.html")

    @staticmethod
    def is_ignored_record(
        rec_file_name: str, rec_header_name: Union[str, None], to_ignore: list[tuple]
    ) -> bool:
        """
        Headers selected by the user as to be ignored from the exclusions.

        Args:
            rec_file_name: The file name as in the search index record, e.g. 'all_dir/all_dir_ignore_heading1/'
            rec_header_name: The header name as in the search index record, e.g. None or
                'single-header-chapter_exclude_heading2-bbex'
            to_ignore: The list of to be ignored (records (from the exclusion) with tuples
                of (rec_file_name, rec_header_name), e.g. ('chapter_exclude_all.md', None)

        Returns:
            True if the record matches with the to_ignore list, False if not.
        """
        return any(
            fnmatch(strip_url_suffix(rec_file_name), strip_md_suffix(file_name))
            and header_name == rec_header_name
            for (file_name, header_name) in to_ignore
        )

    @staticmethod
    def is_excluded_record(
        rec_file_name: str, rec_header_name: Union[str, None], to_exclude: list[tuple]
    ) -> bool:
        """
        Files, headers or directories selected by the user to be excluded.

        Args:
            rec_file_name: The file name as in the search index record, e.g. 'chapter_exclude_all/'
            rec_header_name: The header name as in the search index record, e.g. None or
                'single-header-chapter_exclude_heading2-bbex'
            to_exclude: The list of to be excluded records with tuples of (rec_file_name, rec_header_name),
                e.g. ('chapter_exclude_all.md', None)

        Returns:
            True if the record matches with the to_exclude list, False if not.
        """
        return any(
            fnmatch(strip_url_suffix(rec_file_name), strip_md_suffix(file_name))
            and (rec_header_name == header_name or not header_name)
            for (file_name, header_name) in to_exclude
        )

    def select_included_records(
        self,
        search_index: dict,
        to_exclude: list[tuple[Any, ...]],
        to_ignore: list[tuple[Any, ...]],
        navigation_items: list[str],
        exclude_unreferenced: bool = False,
        exclude_tags: bool = False,
    ) -> list[dict]:
        """
        Select the search index records to be included in the final selection.

        Args:
            search_index: The mkdocs search index in "config.data["site_dir"]) / "search/search_index.json"
            to_exclude: Resolved list of excluded search index records.
            to_ignore: Resolved list of ignored search index chapter records.
            navigation_items: List of markdown filepaths in the mkdocs.yml nav, without the
                markdown suffix, in the format ["filename", "dir/filename"]
            exclude_unreferenced: Boolean wether unreferenced files (not listed in mkdocs nav)
                should be excluded, default False.
            exclude_tags: Boolean wether mkdocs-plugin-tags entries should be excluded, default False.

        Returns:
            A new search index as a list of dicts.
        """
        included_records = []
        for record in search_index["docs"]:
            rec_file_name, rec_header_name = split_header(record["location"])

            if self.is_tag_record(rec_file_name):
                # Tag pages have no markdown file, the unreferenced rule must not apply.
                if exclude_tags:
                    logger.debug(f"exclude-search (excludedTags): {record['location']}")
                    continue
            elif self.is_root_record(rec_file_name):
                included_records.append(record)
                continue
            elif exclude_unreferenced and self.is_unreferenced_record(
                rec_file_name=rec_file_name, navigation_items=navigation_items
            ):
                logger.debug(
                    f"exclude-search (excludedUnreferenced): {record['location']}"
                )
                continue

            if self.is_ignored_record(rec_file_name, rec_header_name, to_ignore):
                logger.debug(f"include-search (ignoredRule): {record['location']}")
                included_records.append(record)
            elif self.is_excluded_record(rec_file_name, rec_header_name, to_exclude):
                logger.debug(f"exclude-search (excludedRule): {record['location']}")
                continue
            else:
                included_records.append(record)

        return included_records

    # pylint: disable=arguments-differ
    def on_post_build(self, config):
        # at mkdocs buildtime, self.config does not contain the same as config
        try:
            self.validate_config(plugins=config["plugins"])
        except ValueError:
            return config

        search_index_fp = Path(config.data["site_dir"]) / "search/search_index.json"
        with open(search_index_fp, encoding="utf-8") as f:
            search_index = json.load(f)

        to_exclude = self.config["exclude"]
        if to_exclude:
            to_exclude = self.resolve_excluded_records(to_exclude=to_exclude)
        to_ignore = self.config["ignore"]
        if to_ignore:
            to_ignore = self.resolve_ignored_chapters(to_ignore=to_ignore)

        if self.config["exclude_unreferenced"] and config.data["nav"] is not None:
            navigation_items = explode_navigation(navigation=config.data["nav"])
        else:
            navigation_items = []

        included_records = self.select_included_records(
            search_index=search_index,
            to_exclude=to_exclude,
            to_ignore=to_ignore,
            navigation_items=navigation_items,
            exclude_unreferenced=self.config["exclude_unreferenced"],
            exclude_tags=self.config["exclude_tags"],
        )

        logger.info(
            f"mkdocs-exclude-search excluded {len(search_index['docs']) - len(included_records)}"
            f" of {len(search_index['docs'])} search index records. Use `mkdocs serve -v` "
            f"for more details."
        )

        search_index["docs"] = included_records
        with open(search_index_fp, "w", encoding="utf-8") as f:
            json.dump(search_index, f)

        return config
