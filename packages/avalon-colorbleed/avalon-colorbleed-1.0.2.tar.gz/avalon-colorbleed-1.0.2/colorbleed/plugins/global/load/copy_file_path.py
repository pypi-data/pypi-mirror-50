import os

from avalon import api


class CopyFilePath(api.Loader):
    """Copy published file path to clipboard"""
    representations = ["*"]
    families = ["*"]

    label = "Copy File Path"
    order = 98
    icon = "clipboard"
    color = "#888888"

    def load(self, context, name=None, namespace=None, data=None):
        self.log.info("Added file path to clipboard: {0}".format(self.fname))
        self.copy_path_to_clipboard(self.fname)

    @staticmethod
    def copy_path_to_clipboard(path):
        from avalon.vendor.Qt import QtCore, QtWidgets

        app = QtWidgets.QApplication.instance()
        assert app, "Must have running QApplication instance"

        # Set to Clipboard
        clipboard = app.clipboard()
        clipboard.setText(os.path.normpath(path))
