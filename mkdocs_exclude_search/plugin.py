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

    config_scheme = (("files", config_options.Type((str, list), default=None)),)

    def __init__(self):
        self.enabled = True
        self.total_time = 0

    def on_post_build(self, config):
        if not "search" in config["plugins"]:
            logger.debug(
                "mkdocs-exclude-search plugin is activated but has no effect as search "
                "plugin is deactivated!"
            )
        else:
            exclude_files = self.config["files"]
            if exclude_files is not None:
                search_index_fp = (
                    Path(config.data["site_dir"]) / "search/search_index.json"
                )
                with open(search_index_fp, "r") as f:
                    search_index = json.load(f)

                included_records = []
                for rec in search_index["docs"]:
                    rec_file_name = (
                        rec["location"].split("/")[0] + "/"
                    )  # Ignore subchapters of excluded files
                    if (
                        rec["location"] not in exclude_files
                        and not rec_file_name in exclude_files
                    ):
                        included_records.append(rec)

                search_index["docs"] = included_records
                with open(search_index_fp, "w") as f:
                    json.dump(search_index, f)

        return config
