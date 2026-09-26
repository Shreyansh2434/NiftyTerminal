"""Backtest configuration dialog."""

from __future__ import annotations

from typing import Any

from ..qt_compat import QT_AVAILABLE, QtWidgets

if QT_AVAILABLE:

    class ConfigurationDialog(QtWidgets.QDialog):
        def __init__(
            self,
            parent: QtWidgets.QWidget | None = None,
            initial: dict[str, Any] | None = None,
        ) -> None:
            super().__init__(parent)
            self.setWindowTitle("Backtest configuration")
            self.setModal(True)
            self.fields: dict[str, QtWidgets.QLineEdit | QtWidgets.QDoubleSpinBox] = {}
            form = QtWidgets.QFormLayout(self)
            values = {
                "symbol": "NIFTY",
                "initial_capital": 100000.0,
                "lot_size": 50.0,
                "entry_days": 5.0,
                "holding_days": 5.0,
                "short_delta": 0.16,
                "wing_width": 150.0,
                "stop_loss_pct": 0.35,
                "target_profit_pct": 0.50,
                "commission_per_contract": 20.0,
                "slippage_bps": 4.0,
                "spread_bps": 10.0,
                "train_days": 126.0,
                "test_days": 63.0,
            }
            values.update(initial or {})
            for key, value in values.items():
                if key == "symbol":
                    widget: QtWidgets.QLineEdit | QtWidgets.QDoubleSpinBox = QtWidgets.QLineEdit(str(value))
                else:
                    widget = QtWidgets.QDoubleSpinBox()
                    widget.setRange(1, 10**12)
                    widget.setDecimals(2)
                    widget.setValue(float(value))
                self.fields[key] = widget
                form.addRow(key.replace("_", " ").title(), widget)
            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.StandardButton.Ok
                | QtWidgets.QDialogButtonBox.StandardButton.Cancel
            )
            buttons.accepted.connect(self.accept)
            buttons.rejected.connect(self.reject)
            form.addRow(buttons)

        def configuration(self) -> dict[str, Any]:
            result: dict[str, Any] = {}
            for key, widget in self.fields.items():
                result[key] = widget.text().strip() if isinstance(widget, QtWidgets.QLineEdit) else widget.value()
            for key in ("lot_size", "entry_days", "holding_days"):
                if key in result:
                    result[key] = int(result[key])
            return result

else:

    class ConfigurationDialog:  # pragma: no cover
        def __init__(self, *_args, **_kwargs) -> None:
            raise RuntimeError("PyQt6 is required to create ConfigurationDialog")
