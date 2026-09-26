"""Optional Qt imports shared by the desktop application."""

from __future__ import annotations

QT_AVAILABLE = False
QT_IMPORT_ERROR: Exception | None = None

try:  # Keep importing the package safe on servers and minimal CI images.
    from PyQt6 import QtCore, QtGui, QtWidgets

    try:
        from PyQt6 import QtCharts  # type: ignore
    except ImportError:  # QtCharts is optional; pyqtgraph is used when present.
        QtCharts = None  # type: ignore[assignment]
    QT_AVAILABLE = True
except ImportError as exc:  # pragma: no cover - exercised on dependency-free CI
    QT_IMPORT_ERROR = exc
    QtCore = None  # type: ignore[assignment]
    QtGui = None  # type: ignore[assignment]
    QtWidgets = None  # type: ignore[assignment]
    QtCharts = None  # type: ignore[assignment]


def missing_qt_message() -> str:
    """Return an actionable installation message for a missing Qt runtime."""

    detail = f" ({QT_IMPORT_ERROR})" if QT_IMPORT_ERROR else ""
    return (
        "The desktop application requires PyQt6. Install desktop dependencies "
        "with `pip install -r requirements.txt` and try again."
        + detail
    )
