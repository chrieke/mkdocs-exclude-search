import json
from pathlib import Path
import logging
from typing import List, Dict
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
            message = f"No excluded search entries selected for mkdocs-exclude-search."
            logger.info(message)
            raise ValueError(message)

    @staticmethod
    def resolve_excluded_records(to_exclude: List[str]) -> List[str]:
        """
        Resolve full search index chapter records from the user provided excluded files,
        chapters and directories ("*").
        """
        to_exclude = [f.replace(".md", ".html") for f in to_exclude]
        # TODO: This currently could exclude files with an excluded folder of the same name.
        for idx, entry in enumerate(to_exclude):
            if "#" in entry:
                to_exclude[idx] = entry.split("#")
            else:
                to_exclude[idx] = [entry, None]
        return to_exclude

    @staticmethod
    def resolve_ignored_chapters(to_ignore: List[str]) -> List[str]:
        """
        Resolve full search index chapter records from the user provided chapter names
        (which should be ignored from the exclusion).
        """
        ignored_chapters = [f.replace(".md", "") for f in to_ignore if ".md" in f]
        # Subchapters require both the subchapter as well as the main record to be
        # included in the search index.
        ignored_main_records = []
        for chapter in ignored_chapters:
            if not chapter.endswith(".md"):
                ignore_entry_main_name = chapter.split("#")[0]
                ignored_main_records.append(ignore_entry_main_name)
        ignored_chapters += ignored_main_records
        return ignored_chapters

    @staticmethod
    def is_tag_record(record: str):
        if "tags.html" in record["location"]:
            # Ignore entries of mkdocs-plugin-tags
            # TODO: Surface in readme
            return True

    @staticmethod
    def select_included_records(
        search_index: Dict,
        to_exclude: List[str],
        to_ignore: List[str],
        exclude_tags: bool = False,
    ) -> List[Dict]:
        """
        Select the search index records to be included in the final selection.
        # TODO: Simplify

        Args:
            search_index: The mkdocs search index in "config.data["site_dir"]) / "search/search_index.json"
            to_exclude: Resolved list of excluded search index records.
            to_ignore: Resolved list of ignored search index chapter records.
            exclude_tags: Boolean if mkdocs-plugin-tags entries should be excluded, default False.

        Returns:
            A new search index
        """
        included_records = []
        for record in search_index["docs"]:
            # check if record is excluded
            try:
                rec_main_name, rec_chapter_name = record["location"].split("#")
            except ValueError:
                rec_main_name, rec_chapter_name = record["location"], None

            if ExcludeSearch.is_tag_record(record) and exclude_tags:
                continue
            elif "/" not in record["location"]:
                # index and other neccessary files.
                included_records.append(record)
                logger.debug(f"include-search (isRoot): {record['location']}")
            # include record if filename and chapter does not match any rule
            elif not any(
                [
                    fnmatch(rec_main_name, x[0])
                    and (
                        rec_chapter_name == x[1]
                        or not x[1]
                    )
                    for x in to_exclude
                ]
            ):
                included_records.append(record)
                logger.debug(f"include-search (byRule): {record['location']}")
            else:
                logger.info(f"exclude-search: {record['location']}")

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
