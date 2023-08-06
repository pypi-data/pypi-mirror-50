# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 16:23:13 2018

@author: samschott
"""
import os.path as osp
import requests
from dropbox.oauth import BadStateException, NotApprovedException
from PyQt5 import QtGui, QtCore, QtWidgets, uic

from dropbox import files

from maestral.main import Maestral
from maestral.oauth import OAuth2Session
from maestral.monitor import CONNECTION_ERRORS
from maestral.config.main import CONF
from maestral.config.base import get_home_dir
from maestral.gui.folders_dialog import FolderItem
from maestral.gui.resources import (APP_ICON_PATH, SETUP_DIALOG_PATH,
                                    get_native_item_icon, get_native_folder_icon)
from maestral.gui.utils import ErrorDialog, icon_to_pixmap


class SetupDialog(QtWidgets.QDialog):

    auth_session = ""
    auth_url = ""

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent=parent)
        # load user interface layout from .ui file
        uic.loadUi(SETUP_DIALOG_PATH, self)

        self.app_icon = QtGui.QIcon(APP_ICON_PATH)

        self.labelIcon.setPixmap(icon_to_pixmap(self.app_icon, 170))
        self.labelIcon_2.setPixmap(icon_to_pixmap(self.app_icon, 70))
        self.labelIcon_3.setPixmap(icon_to_pixmap(self.app_icon, 100))

        self.mdbx = None
        self.folder_items = []

        # rename dialog buttons
        self.buttonBoxAuthCode.buttons()[0].setText("Link")
        self.buttonBoxAuthCode.buttons()[1].setText("Cancel")
        self.buttonBoxDropboxPath.buttons()[0].setText("Select")
        self.buttonBoxDropboxPath.buttons()[0].setDefault(True)
        self.buttonBoxDropboxPath.buttons()[1].setText("Cancel")
        self.buttonBoxDropboxPath.buttons()[2].setText("Unlink")
        self.buttonBoxFolderSelection.buttons()[0].setText("Select")
        self.buttonBoxFolderSelection.buttons()[1].setText("Back")

        # set up combobox
        self.dropbox_location = osp.expanduser("~")
        relative_path = self.rel_path(self.dropbox_location)

        folder_icon = get_native_item_icon(self.dropbox_location)
        self.comboBoxDropboxPath.addItem(folder_icon, relative_path)

        self.comboBoxDropboxPath.insertSeparator(1)
        self.comboBoxDropboxPath.addItem(QtGui.QIcon(), "Other...")
        self.comboBoxDropboxPath.currentIndexChanged.connect(self.on_combobox)
        self.dropbox_folder_dialog = QtWidgets.QFileDialog(self)
        self.dropbox_folder_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        self.dropbox_folder_dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        self.dropbox_folder_dialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
        self.dropbox_folder_dialog.fileSelected.connect(self.on_new_dbx_folder)
        self.dropbox_folder_dialog.rejected.connect(
                lambda: self.comboBoxDropboxPath.setCurrentIndex(0))

        # connect buttons to callbacks
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.pushButtonLink.clicked.connect(self.on_link)
        self.buttonBoxAuthCode.rejected.connect(self.on_reject)
        self.buttonBoxAuthCode.accepted.connect(self.on_auth)
        self.buttonBoxDropboxPath.rejected.connect(self.on_reject)
        self.buttonBoxDropboxPath.accepted.connect(self.on_dropbox_path)
        self.buttonBoxDropboxPath.clicked.connect(self.on_unlink)
        self.buttonBoxFolderSelection.rejected.connect(
                lambda: self.stackedWidget.setCurrentIndex(2))
        self.buttonBoxFolderSelection.accepted.connect(self.on_folder_select)
        self.pushButtonClose.clicked.connect(self.on_accept)
        self.listWidgetFolders.itemChanged.connect(self.update_select_all_checkbox)
        self.selectAllCheckBox.clicked.connect(self.on_select_all_clicked)

        # check if we are already authenticated, skip authentication if yes
        self.auth_session = OAuth2Session()
        if self.auth_session.load_token():

            self.labelDropboxPath.setText("""
            <html><head/><body>
            <p align="left">
            Your Dropbox folder has been moved or deleted from its original location.
            Maestral will not work properly until you move it back. It used to be located
            at: </p><p align="left">{0}</p>
            <p align="left">
            To move it back, click "Quit" below, move the Dropbox folder back to its 
            original location, and launch Maestral again.
            </p>
            <p align="left">
            To re-download your Dropbox, please select a location for your Dropbox 
            folder below. Maestral will create a new folder named "Dropbox" in the
            selected location.</p>          
            <p align="left">
            To unlink your Dropbox account from Maestral, click "Unlink" below.</p>
            </body></html>
            """.format(CONF.get("main", "path")))
            self.buttonBoxDropboxPath.buttons()[1].setText("Quit")
            self.stackedWidget.setCurrentIndex(2)
            Maestral.FIRST_SYNC = False
            self.mdbx = Maestral(run=False)
            self.mdbx.client.get_account_info()

# =============================================================================
# Main callbacks
# =============================================================================

    def closeEvent(self, event):
        if self.stackedWidget.currentIndex == 4:
            self.on_accept()
        else:
            self.on_reject()

    def on_accept(self):
        self.accept()

    def on_reject(self):
        self.mdbx = None
        self.reject()

    def on_unlink(self, b):
        if self.buttonBoxDropboxPath.buttonRole(b) == self.buttonBoxDropboxPath.ResetRole:
            self.mdbx.unlink()
            self.on_reject()

    def on_link(self):
        self.auth_url = self.auth_session.get_auth_url()
        prompt = self.labelAuthLink.text().format(self.auth_url)
        self.labelAuthLink.setText(prompt)

        self.stackedWidget.setCurrentIndex(1)

    def on_auth(self):
        auth_code = self.lineEditAuthCode.text()
        try:
            self.auth_session.verify_auth_key(auth_code)
            self.auth_session.save_creds()
        except requests.HTTPError:
            msg = "Please make sure that you entered the correct authentication code."
            msg_box = ErrorDialog("Authentication failed.", msg, parent=self)
            msg_box.open()
            return
        except BadStateException:
            msg = "The authentication session expired. Please try again."
            msg_box = ErrorDialog("Session expired.", msg, parent=self)
            msg_box.open()
            self.stackedWidget.setCurrentIndex(0)
            return
        except NotApprovedException:
            msg = "Please grant Maestral access to your Dropbox to start syncing."
            msg_box = ErrorDialog("Not approved error.", msg, parent=self)
            msg_box.open()
            return
        except CONNECTION_ERRORS as e:
            msg = "Please make sure that you are connected to the internet and try again."
            msg_box = ErrorDialog("Connection failed.", msg, parent=self)
            msg_box.open()
            return

        # switch to next page
        self.stackedWidget.setCurrentIndex(2)

        # start Maestral after linking to Dropbox account
        Maestral.FIRST_SYNC = False
        self.mdbx = Maestral(run=False)
        self.mdbx.client.get_account_info()

    def on_dropbox_path(self):
        # switch to next page
        self.stackedWidget.setCurrentIndex(3)
        # apply dropbox path
        dropbox_path = osp.join(self.dropbox_location, 'Dropbox')
        self.mdbx.set_dropbox_directory(dropbox_path)
        # populate folder list
        if self.folder_items == []:
            self.populate_folders_list()

    def on_folder_select(self):
        # switch to next page
        self.stackedWidget.setCurrentIndex(4)

        # exclude folders
        excluded_folders = []
        included_folders = []

        for item in self.folder_items:
            if not item.isIncluded():
                excluded_folders.append("/" + item.name.lower())
            elif item.isIncluded():
                included_folders.append("/" + item.name.lower())

        CONF.set("main", "excluded_folders", excluded_folders)

        self.mdbx.get_remote_dropbox_async("")

# =============================================================================
# Helper functions
# =============================================================================

    def on_combobox(self, idx):
        if idx == 2:
            self.dropbox_folder_dialog.open()

    def on_new_dbx_folder(self, new_location):
        self.comboBoxDropboxPath.setCurrentIndex(0)
        if not new_location == '':
            self.comboBoxDropboxPath.setItemText(0, self.rel_path(new_location))
            self.comboBoxDropboxPath.setItemIcon(0, get_native_item_icon(new_location))

        self.dropbox_location = new_location

    def populate_folders_list(self):

        self.listWidgetFolders.addItem("Loading your folders...")

        # add new entries
        root_folders = self.mdbx.client.list_folder("", recursive=False)
        self.listWidgetFolders.clear()

        if root_folders is False:
            self.listWidgetFolders.addItem("Unable to connect. Please try again later.")
            self.self.buttonBoxFolderSelection.buttons()[0].setEnabled(False)
        else:
            self.buttonBoxFolderSelection.buttons()[0].setEnabled(True)

            for entry in root_folders.entries:
                if isinstance(entry, files.FolderMetadata):
                    inc = not self.mdbx.sync.is_excluded_by_user(entry.path_lower)
                    item = FolderItem(entry.name, inc)
                    self.folder_items.append(item)

            for item in self.folder_items:
                self.listWidgetFolders.addItem(item)

        self.update_select_all_checkbox()

    def update_select_all_checkbox(self):
        is_included_list = (i.isIncluded() for i in self.folder_items)
        self.selectAllCheckBox.setChecked(all(is_included_list))

    def on_select_all_clicked(self, checked):
        for item in self.folder_items:
            item.setIncluded(checked)

    @staticmethod
    def rel_path(path):
        """
        Returns the path relative to the users directory, or the absolute
        path if not in a user directory.
        """
        usr = osp.abspath(osp.join(get_home_dir(), osp.pardir))
        if osp.commonprefix([path, usr]) == usr:
            return osp.relpath(path, usr)
        else:
            return path

    def changeEvent(self, QEvent):

        if QEvent.type() == QtCore.QEvent.PaletteChange:
            self.update_dark_mode()

    def update_dark_mode(self):
        # update folder icons: the system may provide different icons in dark mode
        for item in self.folder_items:
            item.setIcon(get_native_folder_icon())

    # static method to create the dialog and return Maestral instance on success
    @staticmethod
    def configureMaestral(parent=None):
        fsd = SetupDialog(parent)
        fsd.exec_()

        return fsd.mdbx
