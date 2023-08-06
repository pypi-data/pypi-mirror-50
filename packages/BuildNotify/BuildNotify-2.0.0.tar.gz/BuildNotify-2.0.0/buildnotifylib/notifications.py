try:
    import pynotify
except ImportError:
    pass
from PyQt5.QtWidgets import QSystemTrayIcon


class Notification(object):
    def __init__(self, widget):
        self.widget = widget
        self.notification = None
        try:
            if pynotify.init(" buildnotify "):
                self.notification = pynotify.Notification("buildnotify", "buildnotify", None)
        except NameError:
            pass

    def show_message(self, title, text):
        if self.notification:
            self.notification.update(title, text, None)
        if self.notification is None or not self.notification.show():
            self.widget.showMessage(title, text, QSystemTrayIcon.Information, 3000)
