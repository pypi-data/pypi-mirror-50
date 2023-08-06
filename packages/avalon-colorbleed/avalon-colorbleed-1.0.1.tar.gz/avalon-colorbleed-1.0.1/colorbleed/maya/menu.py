import sys
import os
import logging

from avalon.vendor.Qt import QtWidgets, QtCore, QtGui

import maya.cmds as cmds

self = sys.modules[__name__]
self._menu = "colorbleed"

log = logging.getLogger(__name__)


def _get_menu():
    """Return the menu instance if it currently exists in Maya"""

    app = QtWidgets.QApplication.instance()
    widgets = dict((w.objectName(), w) for w in app.allWidgets())
    menu = widgets.get(self._menu)
    return menu


def deferred():

    log.info("Attempting to install scripts menu..")

    try:
        import scriptsmenu.launchformaya as launchformaya
        import scriptsmenu.scriptsmenu as scriptsmenu
    except ImportError:
        log.warning("Skipping colorbleed.menu install, because "
                    "'scriptsmenu' module seems unavailable.")
        return

    # load configuration of custom menu
    config_path = os.path.join(os.path.dirname(__file__), "menu.json")
    config = scriptsmenu.load_configuration(config_path)

    # run the launcher for Maya menu
    cb_menu = launchformaya.main(title=self._menu.title(),
                                 objectName=self._menu)

    # apply configuration
    cb_menu.build_from_configuration(cb_menu, config)


def uninstall():

    menu = _get_menu()
    if menu:
        log.info("Attempting to uninstall..")

        try:
            menu.deleteLater()
            del menu
        except Exception as e:
            log.error(e)


def install():

    if cmds.about(batch=True):
        print("Skipping colorbleed.menu initialization in batch mode..")
        return

    uninstall()
    # Allow time for uninstallation to finish.
    cmds.evalDeferred(deferred)


def popup():
    """Pop-up the existing menu near the mouse cursor"""
    menu = _get_menu()

    cursor = QtGui.QCursor()
    point = cursor.pos()
    menu.exec_(point)
