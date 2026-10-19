from PySide6.QtWidgets import QMessageBox, QWidget

from startlive.core.exceptions.WorkerException import WorkerException
from startlive.core.workers.base import Presenter
from startlive.PySide.log import get_logger


class GUIPresenter(Presenter):
    def __init__(self, view: QWidget):
        super().__init__()
        self._view = view
        self.logger = get_logger(self.__class__.__name__)

    def prepare_success_view(self, *args, **kwargs): ...

    def prepare_fail_view(self, exception: Exception):
        if isinstance(exception, WorkerException):
            message = f"{exception.name}线程错误"
            detail = repr(exception.real_exc)
        else:
            message = "工作线程错误"
            detail = repr(exception)
        QMessageBox.critical(self._view, message, detail)

    def prepare_progress_view(self, *args, **kwargs): ...
