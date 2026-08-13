# ------------------------------------------------------------------------------
#  Copyright (c) 2026 Dimitri Kroon.
#  This file is part of plugin.audio.bbcsounds.
#  SPDX-License-Identifier: GPL-3.0-or-later
#  See LICENSE.txt or https://www.gnu.org/licenses/gpl-3.0.txt
# ------------------------------------------------------------------------------

from tests.support import fixtures
fixtures.global_setup()

from unittest import TestCase
from unittest.mock import patch, MagicMock

from resources.lib import favourites

from tests.support.testutils import open_doc, HttpResponse


# noinspection PyPep8Naming
setUpModule = fixtures.setup_local_tests
tearDownModule = fixtures.tear_down_local_tests


class TestFavourites(TestCase):
    @patch('resources.lib.fetch.get', return_value=HttpResponse(text=open_doc('my-sounds.html')()))
    def test_refresh_favourites(self, p_get):
        favs = favourites._Favourites()
        favs.refresh()
        p_get.assert_called_once()
        self.assertEqual(len(favs.subscriptions), 12)
        self.assertEqual(len(favs.bookmarks), 13)