from avalon import api


class CopyFile(api.Loader):
    """Copy the published file to be pasted at the desired location"""

    representations = ["*"]
    families = ["*"]

    label = "Copy File"
    order = 99
    icon = "copy"
    color = "#666666"

    def load(self, context, name=None, namespace=None, data=None):
        self.log.info("Added copy to clipboard: {0}".format(self.fname))
        self.copy_file_to_clipboard(self.fname)

    @staticmethod
    def copy_file_to_clipboard(path):
        from avalon.vendor.Qt import QtCore, QtWidgets

        app = QtWidgets.QApplication.instance()
        assert app, "Must have running QApplication instance"

        # Build mime data for clipboard
        data = QtCore.QMimeData()
        url = QtCore.QUrl.fromLocalFile(path)
        data.setUrls([url])

        # Set to Clipboard
        clipboard = app.clipboard()
        clipboard.setMimeData(data)
