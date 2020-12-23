import markdown
import pytest

from mkdocstrings.extension import MkdocstringsExtension
from mkdocstrings.handlers.base import Handlers
from mkdocstrings.references import fix_refs, relative_url