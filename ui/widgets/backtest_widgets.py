"""Backtest configuration and result widgets."""

from __future__ import annotations

from typing import Any

from ..qt_compat import QT_AVAILABLE, QtCore, QtGui, QtWidgets
from ..utils.formatting import format_currency, format_percent

try:  # pyqtgraph improves the chart when installed, but is not required.
    import pyqtgraph as pg
except ImportError:  # pragma: no cover - expected on minimal installations
    pg = None  # type: ignore[assignment]

if QT_AVAILABLE:

    class BacktestConfigWidget(QtWidgets.QGroupBox):
        """Compact editor for the pure engine's supported configuration."""

        def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
            super().__init__("Configuration", parent)
            self._fields: dict[str, QtWidgets.QAbstractSpinBox | QtWidgets.QLineEdit] = {}
            form = QtWidgets.QFormLayout(self)
            self._add_line(form, "symbol", "Symbol", "NIFTY")
            # QSpinBox uses a signed 32-bit range; this still accommodates
            # realistic account sizes while avoiding platform overflow.
            self._add_spin(form, "initial_capital", "Initial capital", 100000, 1000, 2_000_000_000, 1000)
            self._add_spin(form, "lot_size", "Lot size", 50, 1, 100000, 1)
            self._add_spin(form, "entry_days", "Entry every (days)", 5, 1, 1000, 1)
            self._add_spin(form, "holding_days", "Holding period", 5, 1, 1000, 1)
            self._add_spin(form, "short_delta", "Short delta", 0.16, 0.01, 0.49, 0.01)
            self._add_spin(form, "wing_width", "Wing width", 150, 1, 100000, 25)
            self._add_spin(form, "stop_loss_pct", "Stop loss (%)", 0.35, 0, 10, 0.05)
            self._add_spin(form, "target_profit_pct", "Target profit (%)", 0.50, 0, 10, 0.05)
            self._add_spin(form, "commission_per_contract", "Commission / contract", 20.0, 0, 100000, 1)
            self._add_spin(form, "slippage_bps", "Slippage (bps)", 4.0, 0, 1000, 1)
            self._add_spin(form, "spread_bps", "Spread (bps)", 10.0, 0, 1000, 1)
            self._add_spin(form, "train_days", "Training days", 126, 20, 10000, 10)
            self._add_spin(form, "test_days", "Test days", 63, 1, 10000, 10)

        def _add_line(self, form: QtWidgets.QFormLayout, key: str, label: str, value: str) -> None:
            widget = QtWidgets.QLineEdit(value)
            self._fields[key] = widget
            form.addRow(label, widget)

        def _add_spin(
            self,
            form: QtWidgets.QFormLayout,
            key: str,
            label: str,
            value: int | float,
            minimum: int | float,
            maximum: int | float,
            step: int | float,
        ) -> None:
            if isinstance(value, int):
                widget: QtWidgets.QAbstractSpinBox = QtWidgets.QSpinBox()
                widget.setRange(int(minimum), int(maximum))
                widget.setSingleStep(int(step))
                widget.setValue(value)
            else:
                widget = QtWidgets.QDoubleSpinBox()
                widget.setRange(float(minimum), float(maximum))
                widget.setSingleStep(float(step))
                widget.setDecimals(4)
                widget.setValue(value)
            self._fields[key] = widget
            form.addRow(label, widget)

        def configuration(self) -> dict[str, Any]:
            values: dict[str, Any] = {}
            for key, widget in self._fields.items():
                if isinstance(widget, QtWidgets.QLineEdit):
                    values[key] = widget.text().strip() or "NIFTY"
                elif hasattr(widget, "value"):
                    values[key] = widget.value()
            return values

        def set_configuration(self, values: dict[str, Any]) -> None:
            for key, value in values.items():
                widget = self._fields.get(key)
                if widget is None:
                    continue
                if isinstance(widget, QtWidgets.QLineEdit):
                    widget.setText(str(value))
                elif hasattr(widget, "setValue"):
                    widget.setValue(value)


    class _EquityChart(QtWidgets.QWidget):
        """Small dependency-free equity chart; pyqtgraph is an optional upgrade."""

        def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
            super().__init__(parent)
            self.values: list[float] = []
            self._plot_widget = None
            if pg is not None:
                self._plot_widget = pg.PlotWidget()
                self._plot_widget.setBackground("#111827")
                self._plot_widget.showGrid(x=True, y=True, alpha=0.2)
                self._plot_widget.hideButtons()
                layout = QtWidgets.QVBoxLayout(self)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(self._plot_widget)
            self.setMinimumHeight(170)

        def set_values(self, values: list[float]) -> None:
            self.values = values
            if self._plot_widget is not None:
                self._plot_widget.clear()
                if len(values) >= 2:
                    self._plot_widget.plot(values, pen=pg.mkPen("#22d3ee", width=2))
                return
            self.update()

        def paintEvent(self, event: QtGui.QPaintEvent) -> None:  # type: ignore[name-defined]
            painter = QtGui.QPainter(self)
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
            painter.fillRect(self.rect(), QtGui.QColor("#111827"))
            if len(self.values) < 2:
                painter.setPen(QtGui.QColor("#64748b"))
                painter.drawText(self.rect(), QtCore.Qt.AlignmentFlag.AlignCenter, "No equity data")
                return
            low, high = min(self.values), max(self.values)
            span = max(high - low, 1e-9)
            points = []
            for index, value in enumerate(self.values):
                x = self.width() * index / (len(self.values) - 1)
                y = self.height() - ((value - low) / span * (self.height() - 20)) - 10
                points.append(QtCore.QPointF(x, y))
            painter.setPen(QtGui.QPen(QtGui.QColor("#22d3ee"), 2))
            painter.drawPolyline(points)


    class BacktestResultsWidget(QtWidgets.QWidget):
        """Metrics, equity curve and trades in a single result surface."""

        def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
            super().__init__(parent)
            self.metric_labels: dict[str, QtWidgets.QLabel] = {}
            self.chart = _EquityChart(self)
            self.table = QtWidgets.QTableWidget(0, 6)
            self.table.setHorizontalHeaderLabels(
                ["#", "Entry", "Exit", "Strategy", "Net P&L", "Return"]
            )
            self.table.horizontalHeader().setStretchLastSection(True)
            self.warning = QtWidgets.QLabel()
            self.warning.setWordWrap(True)
            self.warning.setObjectName("warningLabel")
            title = QtWidgets.QLabel("Results")
            title.setObjectName("pageTitle")
            metrics = QtWidgets.QHBoxLayout()
            for key, label in (
                ("total_return_pct", "Total return"),
                ("sharpe", "Sharpe"),
                ("max_drawdown_pct", "Max drawdown"),
                ("win_rate_pct", "Win rate"),
                ("trades", "Trades"),
            ):
                frame = QtWidgets.QFrame()
                frame.setProperty("card", True)
                box = QtWidgets.QVBoxLayout(frame)
                caption = QtWidgets.QLabel(label)
                caption.setObjectName("mutedLabel")
                value = QtWidgets.QLabel("—")
                value.setObjectName("metricValue")
                self.metric_labels[key] = value
                box.addWidget(caption)
                box.addWidget(value)
                metrics.addWidget(frame)
            tabs = QtWidgets.QTabWidget()
            equity = QtWidgets.QWidget()
            equity_layout = QtWidgets.QVBoxLayout(equity)
            equity_layout.addWidget(self.chart)
            tabs.addTab(equity, "Equity")
            trades = QtWidgets.QWidget()
            trades_layout = QtWidgets.QVBoxLayout(trades)
            trades_layout.addWidget(self.table)
            tabs.addTab(trades, "Trades")
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(title)
            layout.addLayout(metrics)
            layout.addWidget(self.warning)
            layout.addWidget(tabs)

        def clear_results(self) -> None:
            for label in self.metric_labels.values():
                label.setText("—")
            self.warning.clear()
            self.chart.set_values([])
            self.table.setRowCount(0)

        def set_results(self, result: dict[str, Any]) -> None:
            metrics = result.get("metrics", {})
            metric_sources = {
                "total_return_pct": "total_return_pct",
                "sharpe": "sharpe_ratio",
                "max_drawdown_pct": "max_drawdown_pct",
                "win_rate_pct": "win_rate",
                "trades": "total_trades",
            }
            for key, label in self.metric_labels.items():
                value = metrics.get(metric_sources[key])
                if value is None and key == "trades":
                    value = len(result.get("trades", []))
                if value is None:
                    label.setText("—")
                elif key.endswith("_pct") or key == "total_return_pct":
                    label.setText(format_percent(value))
                elif key == "sharpe":
                    label.setText(f"{float(value):.2f}")
                else:
                    label.setText(str(value))
            self.warning.setText(result.get("warning") or result.get("error") or "")
            points = [float(row.get("equity", 0)) for row in result.get("equity_curve", [])]
            self.chart.set_values(points)
            rows = result.get("trades", [])
            self.table.setRowCount(len(rows))
            for row_index, trade in enumerate(rows):
                values = (
                    trade.get("trade_number", row_index + 1),
                    trade.get("entry_date", ""),
                    trade.get("exit_date", ""),
                    trade.get("strategy_type", ""),
                    format_currency(trade.get("net_pnl", 0)),
                    format_percent(trade.get("return_pct", 0)),
                )
                for column, value in enumerate(values):
                    self.table.setItem(row_index, column, QtWidgets.QTableWidgetItem(str(value)))

else:

    class BacktestConfigWidget:  # pragma: no cover
        def __init__(self, *_args, **_kwargs) -> None:
            raise RuntimeError("PyQt6 is required to create BacktestConfigWidget")

    class BacktestResultsWidget:  # pragma: no cover
        def __init__(self, *_args, **_kwargs) -> None:
            raise RuntimeError("PyQt6 is required to create BacktestResultsWidget")
