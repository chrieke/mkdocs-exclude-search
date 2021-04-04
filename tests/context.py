import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../mkdocs_exclude_search")
    ),
)

from mkdocs_exclude_search.plugin import ExcludeSearch
