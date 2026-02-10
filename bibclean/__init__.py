"""bibclean package for canonicalizing cited references."""

from .canonicalize import canonicalize_references
from .io.detect import detect_input_format

__all__ = ["canonicalize_references", "detect_input_format"]
