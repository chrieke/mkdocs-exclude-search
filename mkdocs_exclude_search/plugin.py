import json
from pathlib import Path

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin


class ExcludeSearch(BasePlugin):
    """
    Excludes selected nav chapters from the search index.
    """

    config_scheme = (("chapters", config_options.Type((str, list), default=None)),)

    def __init__(self):
        self.enabled = True
        self.total_time = 0

    def on_post_build(self, config):
        if "search" in config["plugins"]:
            exclude_chapters = self.config["chapters"]
            if exclude_chapters is not None:
                search_index_fp = (
                    Path(config.data["site_dir"]) / "search/search_index.json"
                )
                with open(search_index_fp, "r") as f:
                    search_index = json.load(f)
                included_chapters = [
                    c
                    for c in search_index["docs"]
                    if c["title"] not in exclude_chapters
                ]
                search_index["docs"] = included_chapters
                with open(search_index_fp, "w") as f:
                    json.dump(search_index, f)
        return config
