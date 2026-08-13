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

from resources.lib import menu

from tests.support.testutils import open_doc, HttpResponse


# noinspection PyPep8Naming
setUpModule = fixtures.setup_local_tests
tearDownModule = fixtures.tear_down_local_tests


@patch('resources.lib.favourites._Favourites.subscriptions', return_value=set())
@patch('resources.lib.favourites._Favourites.bookmarks', return_value=set())
class ListContainer(TestCase):
    @patch('resources.lib.fetch.get', return_value=HttpResponse(text=open_doc('collection.json')()))
    def test_page_len_tagged_item(self, p_get, _, __):
        list(menu.list_container_content(MagicMock(), 'urn:bbc:radio:tag:dance'))
        call_kwargs = p_get.call_args.kwargs['params']
        self.assertEqual(call_kwargs['limit'], 100)