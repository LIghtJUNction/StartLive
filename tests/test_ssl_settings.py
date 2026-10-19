import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QWidget

from startlive.PySide.window.settings_page import SettingsPage
from startlive.core import app_state
from startlive.core.constant.settings import SettingsName


class SettingsHost(QWidget):
    def switch_tray_icon(self, *_):
        pass

    def switch_tray_hint(self, *_):
        pass


class SslSettingsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_switch_saves_reloads_and_resets(self):
        saved = app_state.app_settings.as_dict()
        self.addCleanup(app_state.app_settings.update, saved)
        app_state.app_settings.reset()
        with tempfile.TemporaryDirectory() as folder:
            def cache_path(kind, filename, **kwargs):
                return Path(folder), Path(folder) / filename

            with patch.object(app_state, "get_cache_path", side_effect=cache_path):
                host = SettingsHost()
                page = SettingsPage(host)
                self.assertFalse(page.ssl_verify_switch.isChecked())
                page.ssl_verify_switch.click()
                self.assertTrue(app_state.app_settings.ssl_verify)
                app_state.app_settings.reset()
                app_state._load_settings(SettingsName.APP)
                self.assertTrue(app_state.app_settings.ssl_verify)
                reopened = SettingsPage(host)
                self.assertTrue(reopened.ssl_verify_switch.isChecked())
                reopened.ssl_verify_switch.click()
                self.assertFalse(app_state.app_settings.ssl_verify)
                app_state.app_settings.update(ssl_verify=True)
                app_state._load_settings(SettingsName.APP)
                self.assertFalse(app_state.app_settings.ssl_verify)
                page.reset_default()
                self.assertFalse(page.ssl_verify_switch.isChecked())
                host.deleteLater()
                self.app.processEvents()
