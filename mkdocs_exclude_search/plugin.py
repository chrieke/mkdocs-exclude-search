import json
from pathlib import Path
import logging
from typing import List, Dict, Tuple, Union, Any
from fnmatch import fnmatch

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.utils import warning_filter


def get_logger():
    """
    Return a pre-configured logger.
    """
    logger = logging.getLogger("mkdocs.plugins.mkdocs-exclude-search")
    logger.addFilter(warning_filter)
    return logger


logger = get_logger()


class ExcludeSearch(BasePlugin):
    """
    Excludes selected nav chapters from the search index.
    """

    config_scheme = (
        ("exclude", config_options.Type((str, list), default=[])),
        ("ignore", config_options.Type((str, list), default=[])),
        ("exclude_tags", config_options.Type(bool, default=False)),
    )

    def __init__(self):
        self.enabled = True
        self.total_time = 0

    @staticmethod
    def check_config(config: dict, to_exclude: List[str], exclude_tags: bool):
        """
        Check plugin configuration.
        """
        if not "search" in config["plugins"]:
            message = (
                "mkdocs-exclude-search plugin is activated but has no effect as "
                "search plugin is deactivated!"
            )
            logger.debug(message)
            raise ValueError(message)
        if not to_exclude and not exclude_tags:
            message = "No excluded search entries selected for mkdocs-exclude-search."
            logger.info(message)
            raise ValueError(message)

    @staticmethod
    def resolve_excluded_records(
        to_exclude: List[str],
    ) -> List:
        """
        Resolve the search index file-name and header-names from the user provided excluded entries.

        Args:
            to_exclude: The user provided list of excluded entries for files,
                headers and directories ("*").

        Returns:
            A list with each resolved entry as a tuple of (file-name, header-name/None).
        """
        excluded_entries = []
        # TODO: This currently could exclude files with an excluded folder of the same name.
        for entry in to_exclude:
            try:
                file_name, header_name = entry.split("#")
            except ValueError:
                file_name, header_name = entry, None  # type: ignore
            excluded_entries.append((file_name, header_name))
        return excluded_entries

    @staticmethod
    def resolve_ignored_chapters(to_ignore: List[str]) -> List:
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
            file_name, header_name = entry.split("#")
            file_name_entries.append((file_name, None))
            file_header_names_entries.append((file_name, header_name))

        ignored_chapters = file_name_entries + file_header_names_entries  # type: ignore
        return ignored_chapters

    @staticmethod
    def is_tag_record(rec_file_name: str):
        """Tags entries of mkdocs-plugin-tags"""
        # TODO: Surface in readme
        if "tags.html" in rec_file_name:
            return True

    @staticmethod
    def is_root_record(rec_file_name: str):
        """Required mkdocs root files"""
        if "/" not in rec_file_name:
            return True

    @staticmethod
    def is_ignored_record(
        rec_file_name: str, rec_header_name: Union[str, None], to_ignore: List[Tuple]
    ):
        """
        Headers selected by the user as to be ignored from the exclusions.

        Args:
            rec_file_name: The file name as in the search index record, e.g. 'all_dir/all_dir_ignore_heading1/'
            rec_header_name: The header name as in the search index record, e.g. None or
                'single-header-chapter_exclude_heading2-bbex'
            to_ignore: The list of to be ignored (records (from the exclusion) with tuples
                of (rec_file_name, rec_header_name), e.g. ('chapter_exclude_all.md', None)

        Returns:
            True if the record matches with the to_ignore list, None if not.
        """
        if any(
            (
                fnmatch(rec_file_name[:-1], f"{file_name.replace('.md', '')}")
                and header_name == rec_header_name
                for (file_name, header_name) in to_ignore
            )
        ):
            return True

    @staticmethod
    def is_excluded_record(
        rec_file_name: str, rec_header_name: Union[str, None], to_exclude: List[Tuple]
    ):
        """
        Files, headers or directories selected by the user to be excluded.

        Args:
            rec_file_name: The file name as in the search index record, e.g. 'chapter_exclude_all/'
            rec_header_name: The header name as in the search index record, e.g. None or
                'single-header-chapter_exclude_heading2-bbex'
            to_exclude: The list of to be excluded records with tuples of (rec_file_name, rec_header_name),
                e.g. ('chapter_exclude_all.md', None)

        Returns:
            True if the record matches with the to_exclude list, None if not.
        """
        if any(
            (
                fnmatch(rec_file_name[:-1], f"{file_name.replace('.md', '')}")
                and (rec_header_name == header_name or not header_name)
                for (file_name, header_name) in to_exclude
            )
        ):
            return True

    def select_included_records(
        self,
        search_index: Dict,
        to_exclude: List[Tuple[Any, ...]],
        to_ignore: List[Tuple[Any, ...]],
        exclude_tags: bool = False,
    ) -> List[Dict]:
        """
        Select the search index records to be included in the final selection.

        Args:
            search_index: The mkdocs search index in "config.data["site_dir"]) / "search/search_index.json"
            to_exclude: Resolved list of excluded search index records.
            to_ignore: Resolved list of ignored search index chapter records.
            exclude_tags: Boolean if mkdocs-plugin-tags entries should be excluded, default False.

        Returns:
            A new search index as a list of dicts.
        """
        included_records = []
        for record in search_index["docs"]:
            try:
                rec_file_name, rec_header_name = record["location"].split("#")
            except ValueError:
                rec_file_name, rec_header_name = record["location"], None

            # pylint: disable=no-else-continue
            if self.is_tag_record(rec_file_name) and exclude_tags:
                logger.info(f"exclude-search (excludedTags): {record['location']}")
                continue
            elif self.is_root_record(rec_file_name):
                logger.debug(f"include-search (requiredRoot): {record['location']}")
                included_records.append(record)
            elif self.is_ignored_record(rec_file_name, rec_header_name, to_ignore):
                logger.info(f"include-search (ignoredRule): {record['location']}")
                included_records.append(record)
            elif self.is_excluded_record(rec_file_name, rec_header_name, to_exclude):
                logger.info(f"exclude-search (excludedRule): {record['location']}")
                continue
            else:
                logger.debug(f"include-search (noRule): {record['location']}")
                included_records.append(record)

        return included_records

    def on_post_build(self, config):
        to_exclude = self.config["exclude"]
        exclude_tags = self.config["exclude_tags"]
        to_ignore = self.config["ignore"]

        try:
            self.check_config(
                config=config, to_exclude=to_exclude, exclude_tags=exclude_tags
            )
        except ValueError:
            return config

        to_exclude = self.resolve_excluded_records(to_exclude=to_exclude)
        if to_ignore:
            to_ignore = self.resolve_ignored_chapters(to_ignore=to_ignore)

        search_index_fp = Path(config.data["site_dir"]) / "search/search_index.json"
        with open(search_index_fp, "r") as f:
            search_index = json.load(f)

        included_records = self.select_included_records(
            search_index=search_index,
            to_exclude=to_exclude,
            to_ignore=to_ignore,
            exclude_tags=exclude_tags,
        )

        search_index["docs"] = included_records
        with open(search_index_fp, "w") as f:
            json.dump(search_index, f)

        return config
