# ------------------------------------------------------------------------------
#  Copyright (c) 2026 Dimitri Kroon.
#  This file is part of plugin.audio.bbcsounds.
#  SPDX-License-Identifier: GPL-3.0-or-later
#  See LICENSE.txt or https://www.gnu.org/licenses/gpl-3.0.txt
# ------------------------------------------------------------------------------

from tests.support import fixtures
fixtures.global_setup()

from unittest import TestCase
from unittest.mock import MagicMock

from resources.lib import parse, plugin
from tests.support.testutils import open_json


SYS_ARGS = ['plugin://plugin.audio.bbcsounds', '1', '', 'resume:false']


# noinspection PyPep8Naming
setUpModule = fixtures.setup_local_tests
tearDownModule = fixtures.tear_down_local_tests


class TestFormatImage(TestCase):
    def test_format_image(self):
        imgurl = 'https://my.server/{recipe}/p0ny9f4c.jpg'
        url = parse.format_img(imgurl)
        self.assertEqual(url, 'https://my.server/512x512/p0ny9f4c.jpg')
        url = parse.format_img(imgurl, 'icon')
        self.assertEqual(url, 'https://my.server/512x512/p0ny9f4c.jpg')
        url = parse.format_img(imgurl, 'fanart')
        self.assertEqual(url, 'https://my.server/1280x720/p0ny9f4c.jpg')


class ParseRail(TestCase):
    def test_homepage_rails(self):
        home_data = open_json('homepage.json')
        rails = home_data['props']['pageProps']['dehydratedState']['queries'][1]['state']['data']['data']
        results = []
        parser = parse.Parser(plugin.Plugin(SYS_ARGS), parent_url='https://bbc.home.page')
        for rail in rails:
            result = parser.parse_rail(rail)
            if result:
                results.append(result)
            self.assertIsInstance(result, (tuple, type(None)))
        # Check that not all items are None.
        self.assertGreater(len([r for r in results if r]), 1)

    def test_parse_rail_with_no_items(self):
        rail = {'id': 'my_id', 'type': 'inline_display_module', 'data': []}
        parser = parse.Parser(plugin.Plugin(SYS_ARGS), parent_url='https://bbc.home.page')
        result = parser.parse_rail(rail)
        self.assertIsNone(result)


class ParsePlayableItem(TestCase):
    def test_parse_live_playables_from_homepage(self):
        home_data = open_json('homepage.json')
        rails = home_data['props']['pageProps']['dehydratedState']['queries'][1]['state']['data']['data']
        parser = parse.Parser(MagicMock(), 'my.url')
        for rail in rails:
            if rail['id'] == 'listen_live':
                live_items = rail['data']
                for item in live_items:
                    result = parser.parse_playable_item(item)
                    self.assertIsInstance(result, tuple)
                    self.assertTrue(result[0].startswith("plugin://plugin.audio.bbcsounds/"))
                    self.assertFalse(result[2])
                    li = result[1]
                    self.assertEqual(li._path_, result[0])
                    self.assertEqual(li._props_['IsPlayable'], 'true')
                return
        assert False

    def test_parse_live_playables_from_stations(self):
        stations_data = open_json('stations.json')
        # NOTE: This data structure has only one queries member.
        rails = stations_data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']
        parser = parse.Parser(MagicMock(), 'my.url')
        for rail in rails:
            parser.container_type = rail['id']
            live_items = rail['data']
            for item in live_items:
                callb_url, listitem, is_folder = parser.parse_playable_item(item)
                self.assertTrue(callb_url.startswith("plugin://plugin.audio.bbcsounds/"))
                self.assertFalse(is_folder)
                self.assertEqual(listitem._path_, callb_url)
                self.assertEqual(listitem._props_['IsPlayable'], 'true')
            return
        assert False
