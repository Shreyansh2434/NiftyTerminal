"""Native PyQt6 desktop application for the NIFTY options terminal.

The package deliberately keeps Qt imports optional.  This means command-line
tools, the web application, and documentation builds can import ``ui`` even
when desktop dependencies are not installed.
"""

from .qt_compat import QT_AVAILABLE

__all__ = ["QT_AVAILABLE"]
