"""Modal dialogs used by the desktop application."""

from .backtest_config_dialog import BacktestConfigDialog
from .config_dialog import ConfigurationDialog
from .settings_dialog import SettingsDialog
from .strategy_builder_dialog import StrategyBuilderDialog
from .execution_config_dialog import ExecutionConfigDialog
from .alert_config_dialog import AlertConfigDialog

__all__ = ["ConfigurationDialog", "BacktestConfigDialog", "SettingsDialog", "StrategyBuilderDialog", "ExecutionConfigDialog", "AlertConfigDialog"]
