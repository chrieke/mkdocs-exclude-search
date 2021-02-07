import json
from pathlib import Path
import logging

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

    def on_post_build(self, config):
        if not "search" in config["plugins"]:
            logger.debug(
                "mkdocs-exclude-search plugin is activated but has no effect as search "
                "plugin is deactivated!"
            )
            return config

        to_exclude = self.config["exclude"]
        to_ignore = self.config["ignore"]
        exclude_tags = self.config["exclude_tags"]

        if not to_exclude or not exclude_tags:
            logger.info(
                f"To exclude search entries please add any files to the mkdocs-exclude-search plugin configuration."
            )
            return config

        # Find files to ignore from ignore user config.
        if to_ignore:
            to_ignore = [f.replace(".md", "") for f in to_ignore if ".md" in f]
            # subchapters require both the subchapter as well as the main record.
            also_ignore = []
            for ignore_entry in to_ignore:
                if not ignore_entry.endswith(".md"):
                    ignore_entry_main_name = ignore_entry.split("#")[0]
                    also_ignore.append(ignore_entry_main_name)
            to_ignore += also_ignore

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
