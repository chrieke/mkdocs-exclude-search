import json
from pathlib import Path
import logging
from typing import List

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
    def resolve_ignored_chapters(to_ignore: List[str]) -> List[str]:
        """
        Resolve full search index chapter entries from the user provided chapter names
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

        if to_ignore:
            to_ignore = self.resolve_ignored_chapters(to_ignore)

        # Find filenames of directory exclusions via "*"
        to_exclude = [f.replace(".md", "") for f in to_exclude if ".md" in f]
        # TODO: This currently could exclude files with an excluded folder of the same name.
        for idx, entry in enumerate(to_exclude):
            if "*" in entry:
                to_exclude[idx] = "".join(entry.split("/")[:-1])

        search_index_fp = Path(config.data["site_dir"]) / "search/search_index.json"
        with open(search_index_fp, "r") as f:
            search_index = json.load(f)

        included_records = []
        for rec in search_index["docs"]:
            if "/" not in rec["location"]:
                if "tags.html" in rec["location"] and exclude_tags:
                    # Ignore entries of mkdocs-plugin-tags
                    # TODO: Surface in readme
                    continue
                # index and other neccessary files.
                included_records.append(rec)
            else:
                if len(rec["location"].split("/")) > 2:
                    rec_dir = "".join(rec["location"].split("/")[:-2])
                else:
                    rec_dir = None
                rec_main_name, rec_subchapter = rec["location"].split("/")[-2:]

                if rec_main_name + rec_subchapter in to_ignore:
                    # print("ignored", rec["location"])
                    included_records.append(rec)
                elif (
                    rec_dir not in to_exclude
                    and rec_main_name not in to_exclude
                    and rec_main_name + rec_subchapter
                    not in to_exclude  # Also ignore subchapters of excluded main records
                ):
                    # print("included", rec["location"])
                    included_records.append(rec)
                else:
                    logger.info(f"exclude-search: {rec['location']}")

        search_index["docs"] = included_records
        with open(search_index_fp, "w") as f:
            json.dump(search_index, f)

        return config
