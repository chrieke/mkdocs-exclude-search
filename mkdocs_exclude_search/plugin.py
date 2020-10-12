import os
import sys
from timeit import default_timer as timer
from datetime import datetime, timedelta
import json

from .lyrics import random_lyrics

from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin

class ExcludeSearch(BasePlugin):
    """
    Excludes files from the search index.

    https://github.com/mkdocs/mkdocs/issues/773

    mkdocs/mkdocs/commands/build.py
    Line 251
    search_index.add_entry_from_context(

    Check variable and remove.
    """
    config_scheme = (
        ('chapters', config_options.Type((str, list), default=None)),
    )

    def __init__(self):
        self.enabled = True
        self.total_time = 0

    def on_post_build(self, config):
        chapters = self.config['chapters']
        if chapters is not None:
            # read json
            with open('path_to_file/person.json') as f:
                data = json.load(f)

            # replace

            # write json
            # with open('person.txt', 'w') as json_file:
            #     json.dump(person_dict, json_file)

        return config
    # def on_page_markdown(self, markdown, page, config, site_nav):
    #
    #     # hello dolly example https://github.com/fmaida/hello-dolly-mkdocs-plugin
    #     markdown = markdown.replace("{{dolly}}", random_lyrics())
    #     return markdown

