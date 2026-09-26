"""Trading tab widgets (data-provider independent, with clear empty states)."""

from __future__ import annotations

from ..qt_compat import QT_AVAILABLE, QtCore, QtWidgets

if QT_AVAILABLE:

    class TradingDashboard(QtWidgets.QWidget):
        """A native overview that remains useful when market data is offline."""

        def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
            super().__init__(parent)
            self._build_ui()

        def _build_ui(self) -> None:
            title = QtWidgets.QLabel("Trading dashboard")
            title.setObjectName("pageTitle")
            subtitle = QtWidgets.QLabel(
                "Live market data is optional. Use the Backtest tab for local analysis."
            )
            subtitle.setObjectName("mutedLabel")
            self.refresh_button = QtWidgets.QPushButton("Refresh snapshot")
            self.refresh_button.clicked.connect(self._refresh)
            self.connection_label = QtWidgets.QLabel("●  Offline / not connected")
            self.connection_label.setObjectName("warningLabel")

            cards = QtWidgets.QHBoxLayout()
            for label, value in (
                ("NIFTY spot", "—"),
                ("Market regime", "—"),
                ("PCR", "—"),
                ("Max pain", "—"),
            ):
                frame = QtWidgets.QFrame()
                frame.setProperty("card", True)
                box = QtWidgets.QVBoxLayout(frame)
                name = QtWidgets.QLabel(label)
                name.setObjectName("mutedLabel")
                number = QtWidgets.QLabel(value)
                number.setObjectName("metricValue")
                box.addWidget(name)
                box.addWidget(number)
                cards.addWidget(frame)

            notice = QtWidgets.QTextBrowser()
            notice.setOpenExternalLinks(False)
            notice.setPlainText(
                "No live snapshot has been loaded. The desktop client does not "
                "start or require the web server; connect your own data provider "
                "when one is available."
            )
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(title)
            layout.addWidget(subtitle)
            layout.addLayout(cards)
            controls = QtWidgets.QHBoxLayout()
            controls.addWidget(self.refresh_button)
            controls.addWidget(self.connection_label)
            controls.addStretch()
            layout.addLayout(controls)
            layout.addWidget(notice)
            layout.addStretch()

        def _refresh(self) -> None:
            self.connection_label.setText("●  No provider configured")
            self.connection_label.setObjectName("warningLabel")
            self.style().unpolish(self.connection_label)
            self.style().polish(self.connection_label)

else:

    class TradingDashboard:  # pragma: no cover
        def __init__(self, *_args, **_kwargs) -> None:
            raise RuntimeError("PyQt6 is required to create TradingDashboard")
