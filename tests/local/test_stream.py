# ------------------------------------------------------------------------------
#  Copyright (c) 2026 Dimitri Kroon.
#  This file is part of plugin.audio.bbcsounds.
#  SPDX-License-Identifier: GPL-3.0-or-later
#  See LICENSE.txt or https://www.gnu.org/licenses/gpl-3.0.txt
# ------------------------------------------------------------------------------

from tests.support import fixtures
fixtures.global_setup()

from unittest import TestCase
from unittest.mock import patch

from resources.lib import stream
from tests.support.testutils import open_json, open_doc, HttpResponse


# noinspection PyPep8Naming
setUpModule = fixtures.setup_local_tests
tearDownModule = fixtures.tear_down_local_tests


class GetJwt(TestCase):
    @patch('resources.lib.fetch.get', return_value=HttpResponse(text=open_doc('live_bbc-one.html')()))
    def test_get_jwt_for_live(self, p_get):
        resp = stream.get_jwt('http://path.to.bbc-one')
        self.assertIsInstance(resp, str)
        self.assertGreater(len(resp), 16)