# ------------------------------------------------------------------------------
#  Copyright (c) 2022-2026 Dimitri Kroon.
#  This file is part of plugin.audio.bbcsounds.
#  SPDX-License-Identifier: GPL-3.0-or-later
#  See LICENSE.txt or https://www.gnu.org/licenses/gpl-3.0.txt
# ------------------------------------------------------------------------------
from __future__ import annotations
import os
import sys
import re
from typing import Dict, List, Tuple
from urllib.parse import urlencode
from unittest import TestCase
from unittest.mock import patch, MagicMock
from collections.abc import Callable

import xbmc
import xbmcvfs
import xbmcgui
import xbmcaddon

from resources.lib import plugin


patch_g = None

ADDON_ID = 'plugin.audio.bbcsounds'


def global_setup():
    """Fixture required for all test.
    Ensure this is imported and called in every test module first thing. At least before
    importing any other module from the project or other kodi related module.

    As it is global for all tests there is no need to tear down.

    """
    global patch_g
    if patch_g is None:
        # Ensure that kodi's special://profile refers to a predefined folder. Just in case
        # some code want to write, whether intentional or not.
        profile_dir = os.path.normpath(os.path.join(str(os.path.dirname(__file__)), '..', 'addon_profile_dir'))
        info_map = {'profile': profile_dir,
                    'id': ADDON_ID,
                    'name': 'BBC Sounds'}
        patch_g = patch('xbmcaddon.Addon.getAddonInfo',
                         new=lambda self, item: info_map.get(item, ''))
        patch_g.start()

        # Translate callb_path with special:// protocol to a callb_path in the kodifs directory on the
        # top of out test folder.
        xbmcvfs.translatePath = translate_path_mock
        xbmcvfs.File = FileMock
        xbmcaddon.Addon.getLocalizedString = localise_mock
        xbmc.log = print_log

        # Use an xbmcgui.ListItem that stores the values which have been set.
        patch_listitem()


patch_1 = None


class RealWebRequestMadeError(Exception):
    pass


def setup_local_tests():
    """Module level fixture for all local tests. Ensures that no unintentional real
    web requests can occur.

    """
    global patch_1
    patch_1 = patch('requests.sessions.Session.send', side_effect=RealWebRequestMadeError)
    patch_1.start()


def tear_down_local_tests():
    global patch_1

    if patch_1:
        patch_1.stop()
        patch_1 = None




credentials_set = False


def ensure_signed_in() -> None:
    # IMPORTANT: import here, after global setup has been executed and paths to addon profile_dir are set!!
    from resources.lib import account

    global credentials_set
    if credentials_set:
        return

    cookies_file = os.path.join(xbmcaddon.Addon().getAddonInfo('profile'), 'cookies.txt')
    try:
        with open(cookies_file, 'r') as f:
            cookies = f.read()
            if 'ckns_rtkn="' in cookies and 'ckns_atkn="' in cookies:
                credentials_set = True
                return
    except OSError as err:
        pass

    try:
        from tests import credentials
    except ImportError:
        raise RuntimeError("Missing BBC account credentials.")

    with account.LoginSession() as login_session:
        credentials_set = (login_session.check_email(credentials.uname)
                           and login_session.sign_in_with_password(credentials.passw))

    if not credentials_set:
        import traceback
        traceback.print_exc()
        sys.exit(1)


def setup_web_test(*args):
    # Sign in once per test run.
    if not credentials_set:
        ensure_signed_in()


def print_log(message: str, level: int) -> None:
    print(message)


# noinspection PyPep8Naming
class ListItemMock(xbmcgui.ListItem):
    def __init__(self, label: str = "",
                 label2: str = "",
                 path: str = "",
                 offscreen: bool = False) -> None:
        super().__init__()
        assert isinstance(label, str)
        assert isinstance(label2, str)
        assert isinstance(path, str)
        assert isinstance(offscreen, bool)
        self._label = label
        self._label2 = label2
        self._path_ = path
        self._offscreen_ = offscreen
        self._is_folder_ = False
        self._art = {}
        self._info = {}
        self._props_ = {}

    def getLabel(self) -> str:
        return self._label

    def getLabel2(self) -> str:
        return self._label2

    def setLabel(self, label: str) -> None:
        assert isinstance(label, str), "Argument 'label' must be a string."
        self._label = label

    def setLabel2(self, label: str) -> None:
        assert isinstance(label, str), "Argument 'label' must be a string."
        self._label2 = label

    def setArt(self, dictionary: Dict[str, str]) -> None:
        assert isinstance(dictionary, dict), "Argument 'dictionary' must be a dict."
        self._art.update(dictionary)

    def setIsFolder(self, isFolder: bool) -> None:
        assert isinstance(isFolder, bool), "Argument 'isFolder' must be a boolean."
        self._is_folder_ = isFolder

    # noinspection shadowing-builtins
    def setInfo(self, type: str, infoLabels: Dict[str, str]) -> None:
        assert isinstance(type, str), "Argument 'type' must be a string."
        assert isinstance(infoLabels, dict), "Argument 'infoLabels' must be a dict."
        assert type in ('video', 'music', 'pictures', 'game')
        info_dict = self._info.setdefault(type, {})
        info_dict.update(infoLabels)

    def setProperty(self, key: str, value: str) -> None:
        assert isinstance(key, str), "Argument 'key' must be a string."
        assert isinstance(value, str), "Argument 'value' must be a string."
        self._props_[key] = value

    def setProperties(self, dictionary: Dict[str, str]) -> None:
        assert isinstance(dictionary, dict), "Argument 'dictionary' must be a dict."
        self._props_.update(dictionary)

    def getProperty(self, key: str) -> str:
        assert isinstance(key, str), "Argument 'key' must be a string."
        return self._props_['key']

    def setPath(self, path: str) -> None:
        assert isinstance(path, str), "Argument 'callb_path' must be a string."
        self._path_ = path

    def setMimeType(self, mimetype: str) -> None:
        assert isinstance(mimetype, str), "Argument 'mimetype' must be a string."
        self._mimetype = mimetype

    def setContentLookup(self, enable: bool) -> None:
        assert isinstance(enable, bool), "Argument 'enable' must be a boolean."
        self._content_lookup = enable

    def setSubtitles(self, subtitleFiles: List[str] | tuple[str]) -> None:
        assert isinstance(subtitleFiles, (list, tuple)), "Argument 'subtitleFiles' must be a tuple or a list."
        self._subtitles = subtitleFiles

    def getPath(self) -> str:
        return self._path_

    def __repr__(self):
        return f"<ListItem(label='{self._label}', path='{self._path_}>'"


def patch_listitem():
    xbmcgui.ListItem = ListItemMock


class ListItemCollectorBase:
    """Object intended to patch xbmcplugin.addDirectoryItem, store all calls
    and provide easier access than a standard Mock."""
    def __init__(self):
        self._call_args = []

    @property
    def calls(self) -> list[tuple[str, ListItemMock, bool]]:
        return self._call_args

    @property
    def paths(self) -> list[str]:
        return [call[0] for call in self._call_args]

    def path(self, index) -> str:
        return self._call_args[index][0]

    @property
    def list_items(self) -> list[ListItemMock]:
        return [call[1] for call in self._call_args]

    def list_item(self, index) -> ListItemMock:
        return self._call_args[index][1]

    def append(self, item: Tuple[str, xbmcgui.ListItem, bool]):
        url, listitem, isFolder = item
        if not isinstance(url, str):
            raise TypeError(f"'url' must be a string, not {type(url).__name__}, in directory item {item}.")
        if not isinstance(listitem, xbmcgui.ListItem):
            raise TypeError(
                f"'listitem' must be an xbmcgui.ListItem, not {type(listitem).__name__}, in directory item  {item}.")
        if not isinstance(isFolder, bool):
            raise TypeError(f"'isFolder' must be a boolean, not {type(isFolder).__name__}, in directory item {item}.")
        self._call_args.append(item)

    def __len__(self):
        return len(self._call_args)

    def __iter__(self):
        return iter(self.list_items)

    def __getitem__(self, item):
        return self._call_args[item]


class ListItemCollector(ListItemCollectorBase):
    """Object intended to patch xbmcplugin.addDirectoryItem, store all calls,
    and provide easier access than a standard Mock.

    """

    # noinspection pep8-naming
    def __call__(self,
                 handle: int,
                 url: str,
                 listitem: xbmcgui.ListItem,
                 isFolder: bool):
        self.append((url, listitem, isFolder))


class ListItemsCollector(ListItemCollectorBase):
    """Object intended to patch xbmcplugin.addDirectoryItems (plural).
     Store all calls and provide easier access than a standard Mock.

    """

    # noinspection pep8-naming
    def __call__(self,
                 handle: int,
                 items: list[tuple[str, xbmcgui.ListItem, bool]],
                 totalItems: int = 0):
        for item in items:
            if not isinstance(item, tuple):
                raise TypeError(
                    f"Invalid directory item '{item}': must be tuple[str, ListItem, bool], not {type(item).__name__}.")
            self.append(item)
        if len(self._call_args) > totalItems:
            raise ValueError("xbmcplugin.addDirectoryItems has more items than specified in totalItems.")


def translate_path_mock(path: str):
    """Translate 'special://' paths to folders in a directory named 'kodifs' in the top
    test directory, assuming this file is in a folder directly under test/.

    It is not accurate enough to reliably translate every possible special callb_path, but it's
    enough to suit our needs right now.
    """
    if not path.startswith('special://'):
        return path
    special_path = path[10:]
    test_base = os.path.normpath(os.path.join(str(os.path.dirname(__file__)), '..', 'kodifs'))
    special_base_dir = special_path.split('/', 1)[0]
    os.makedirs(os.path.join(test_base, special_base_dir), exist_ok=True)
    local_dir = os.path.join(test_base, special_path)
    return local_dir


# noinspection PyUnusedLocal,unused-parameter
def localise_mock(self, str_id):
    """Return the text corresponding to str_id in the original language file.
    Returns only the text of the first line in the file.

    """
    if 30000 <= str_id <= 30999:
        pattern = f'msgctxt "#{str_id}"\nmsgid "([^"]*)"'
        test_dir = os.path.normpath(os.path.join(str(os.path.dirname(__file__)), '../'))
        lang_file = os.path.join(
            test_dir,
            f'../resources/language/resource.language.en_gb/strings.po')
        with open(lang_file) as f:
            lang_texts = f.read()
        match = re.search(pattern, lang_texts)
        if match:
            return match[1]
        return ''
    else:
        return f'SYS_STRING<{str_id}>'


# noinspection pep8-naming
class FileMock(xbmcvfs.File):
    def __init__(self, filepath: str, mode: str | None = None) -> None:
        super().__init__(filepath, mode)    # doesn't do anything, but keeps pycharm happy.
        if mode is None:
            mode = 'r'
        self._file = open(translate_path_mock(filepath), mode)

    def read(self, numBytes: int = 0) -> str:
        # For some reason Kodi's default numBytes == 0, while Python requires -1 to read all content.
        if numBytes == 0:
            numBytes = -1
        return self._file.read(numBytes)

    def write(self, buffer: str | bytes | bytearray) -> bool:
        return bool(self._file.write(buffer))

    def close(self) -> None:
        self._file.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AddonRunner(TestCase):
    def __init__(self, *args, **kwargs):
        self.subscriptions = kwargs.pop('subscriptions', [])
        self.bookmarks = kwargs.pop('bookmarks', [])
        super().__init__(*args, **kwargs)

    def setUp(self):
        self._subs_patch = patch('resources.lib.favourites._Favourites.subscriptions',
                                 return_value=set(self.subscriptions))
        self._bookm_patch = patch('resources.lib.favourites._Favourites.bookmarks',
                                  return_value=set(self.bookmarks))
        self._subs_patch.start()
        self._bookm_patch.start()

    def tearDown(self) -> None:
        self._subs_patch.stop()
        self._bookm_patch.stop()

    @staticmethod
    def create_argv(module: str, function: str, **kwargs):
        path = '/'.join(('plugin://plugin.audio.bbcsounds', module, function))
        qs = urlencode(kwargs)
        return [path, '1', '?' + qs if qs else '', 'resume:false']

    def run_addon(self,
                  argv: list[str],
                  patched_request: MagicMock | None = None,
                  items_count: int | None = None,
                  items_min: int | None = None,
                  items_max: int | None = None) -> ListItemsCollector:
        with patch('xbmcplugin.addDirectoryItems', ListItemsCollector()) as items_collector:
            addon = plugin.Plugin(argv)
            addon.run()
            if patched_request:
                patched_request.assert_called_once()
            if items_count:
                self.assertEqual(items_count, len(items_collector))
            elif items_min:
                self.assertGreaterEqual(len(items_collector), items_min)
            elif items_max:
                self.assertLessEqual(len(items_collector), items_max)
        return items_collector

    def run_callback(self,
                     callb_func: Callable[..., tuple[str, xbmcgui.ListItem, bool] | None],
                     callb_kwargs: dict | None = None,
                     patched_request: MagicMock | None = None,
                     items_count: int | None = None,
                     items_min: int | None = None,
                     items_max: int | None = None) -> ListItemsCollector:
        callb_module = callb_func.__module__
        assert callb_module.startswith('resources.lib.')
        callb_module = callb_module[14:]
        callb_name = callb_func.__name__
        if not callb_kwargs:
            callb_kwargs = {}
        argv = self.create_argv(callb_module, callb_name, **callb_kwargs)
        return self.run_addon(argv, patched_request, items_count, items_min, items_max)
