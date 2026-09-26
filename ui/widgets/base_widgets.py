"""Dense, reusable Bloomberg-style Qt widgets."""
from __future__ import annotations

from ..qt_compat import QT_AVAILABLE, QtCore, QtWidgets

if QT_AVAILABLE:

    class DenseCard(QtWidgets.QFrame):
        def __init__(self, title: str = "", parent=None):
            super().__init__(parent)
            self.setObjectName("denseCard")
            layout = QtWidgets.QVBoxLayout(self)
            layout.setContentsMargins(8, 8, 8, 8)
            layout.setSpacing(4)
            if title:
                heading = QtWidgets.QLabel(title.upper())
                heading.setObjectName("cardTitle")
                layout.addWidget(heading)
                divider = QtWidgets.QFrame()
                divider.setFrameShape(QtWidgets.QFrame.Shape.HLine)
                divider.setObjectName("cardDivider")
                layout.addWidget(divider)
            self.content_layout = QtWidgets.QVBoxLayout()
            self.content_layout.setSpacing(4)
            layout.addLayout(self.content_layout)

    class MetricRow(QtWidgets.QWidget):
        def __init__(self, label: str, value: str, is_positive: bool | None = None, parent=None):
            super().__init__(parent)
            layout = QtWidgets.QHBoxLayout(self)
            layout.setContentsMargins(0, 2, 0, 2)
            layout.setSpacing(8)
            name = QtWidgets.QLabel(label)
            name.setObjectName("metricLabel")
            result = QtWidgets.QLabel(value)
            result.setObjectName("metricPositive" if is_positive is True else "metricNegative" if is_positive is False else "metricValue")
            result.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
            layout.addWidget(name)
            layout.addStretch()
            layout.addWidget(result)

    class DenseDataTable(QtWidgets.QTableWidget):
        def __init__(self, columns: list[str], parent=None):
            super().__init__(0, len(columns), parent)
            self.setObjectName("denseTable")
            self.setHorizontalHeaderLabels(columns)
            self.verticalHeader().setDefaultSectionSize(20)
            self.verticalHeader().setVisible(False)
            self.horizontalHeader().setStretchLastSection(False)
            self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
            self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
            self.setShowGrid(True)
            for index in range(len(columns)):
                self.horizontalHeader().setSectionResizeMode(index, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

    class HoverButton(QtWidgets.QPushButton):
        def __init__(self, text: str, parent=None):
            super().__init__(text, parent)
            self.setObjectName("compactButton")

else:
    class DenseCard:  # pragma: no cover
        def __init__(self, *_args, **_kwargs): raise RuntimeError("PyQt6 is required")
    MetricRow = DenseDataTable = HoverButton = DenseCard
