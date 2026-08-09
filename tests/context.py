import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../mkdocs_exclude_search")
    ),
)

from plugin import ExcludeSearch
from utils import (
    explode_navigation,
    iterate_all_values,
    split_header,
    strip_md_suffix,
    strip_url_suffix,
)
