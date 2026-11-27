# ------------------------------------------------------------------------------
#  Copyright (c) 2026 Dimitri Kroon.
#  This file is part of plugin.audio.bbcsounds.
#  SPDX-License-Identifier: GPL-3.0-or-later
#  See LICENSE.txt or https://www.gnu.org/licenses/gpl-3.0.txt
# ------------------------------------------------------------------------------
from __future__ import annotations
from tests.support import fixtures

from unittest.mock import patch

from resources.lib import stream
from resources.lib import menu

from web.test_account import MockedCookieJar


class TestPages(fixtures.WebTestCase):
    def test_home_page(self):
        argv = self.create_argv('menu', 'list_page', page_url='https://www.bbc.co.uk/sounds')
        self.run_addon(argv, items_min=8)

    def test_music_page(self):
        argv = self.create_argv('menu', 'list_page', page_url='https://www.bbc.co.uk/sounds/music')
        self.run_addon(argv, items_min=7)

    def test_podcast_page(self):
        argv = self.create_argv('menu', 'list_page', page_url='https://www.bbc.co.uk/sounds/podcasts')
        self.run_addon(argv, items_min=10)

    def test_mysounds_page(self):
        argv = self.create_argv('menu', 'list_page', page_url='https://www.bbc.co.uk/sounds/my')
        self.run_addon(argv, items_count=4)

    def test_live_stations_page(self):
        argv = self.create_argv('menu', 'list_page', page_url='https://www.bbc.co.uk/sounds/stations')
        self.run_addon(argv, items_count=2)


class TestRail(fixtures.WebTestCase):
    def test_main_page_rail_content(self):
        for rail_id in (
                # 'listen_live',
                'continue_listening',
                'unmissable_speech',
                'unmissable_music',
                'latest_playables_for_curation-m001bm45',
                'editorial_collection',
                'local_rail',
                'collections',
                'categories',):
            items = self.run_callback(
                    menu.list_rail,
                    page_url='https://www.bbc.co.uk/sounds',
                    rail_id=rail_id)
            self.assertGreater(len(items), 6)

    @patch('resources.lib.fetch.cookie_jar', MockedCookieJar)
    def test_main_page_rail_not_signed_in(self):
        rail_id = 'unmissable_speech'
        items = self.run_callback(
            menu.list_rail,
            page_url='https://www.bbc.co.uk/sounds',
            rail_id=rail_id)
        self.assertGreater(len(items), 6)

    def test_podcasts_rail_content(self):
        for rail_id in (
                'speech_page_curations',
                'speech_page_featured_rail',
                'speech_page_recommended_podcasts-we-love',
                'speech_page_recommended_all-time-favourites',
                'container_list_podcasts_factual-crimeandjustice-truecrime',
                'container_list_podcasts_factual-lifestories',
                'container_list_podcasts_factual-history',
                'container_list_podcasts_factual-scienceandnature',
                'container_list_podcasts_comedy',
                'container_list_podcasts_sport',
                'container_list_podcasts',):
            argv = self.create_argv('menu', 'list_rail', page_url='https://www.bbc.co.uk/podcasts', rail_id=rail_id)
            self.run_addon(argv, items_min=6)

    def test_live_stations_rail_content(self,):
        # National stations
        argv = self.create_argv('menu', 'list_rail',
                                page_url='https://www.bbc.co.uk/sounds/stations',
                                rail_id='national_and_regional_stations')
        self.run_addon(argv, items_min=10)


class ContainerContent(fixtures.WebTestCase):
    def test_news_summary_page(self, ):
        argv = self.create_argv('menu', 'list_container_content', urn='urn:bbc:radio:brand:p0ddbgqd')
        self.run_addon(argv, items_min=20)

    def test_series(self):
        self.run_callback(menu.list_container_content, urn='urn:bbc:radio:series:m001rgzp')

    def test_collection(self):
        col_id =  'p0dmj1v8'    # collection "Discover podcasts"
        items = list(self.run_callback(menu.list_container_content, urn=f'urn:bbc:radio:collection:{col_id}'))
        self.assertGreater(len(items), 6)

    @patch('resources.lib.fetch.cookie_jar', MockedCookieJar)
    def test_collection_not_signed_in(self):
        col_id =  'p0dmj1v8'    # collection "Discover podcasts"
        items = list(self.run_callback(menu.list_container_content, urn=f'urn:bbc:radio:collection:{col_id}'))
        self.assertGreater(len(items), 6)

    @patch('resources.lib.fetch.cookie_jar', MockedCookieJar)
    def test_collection_not_signed_in_without_settings(self):
        col_id =  'p0dmj1v8'    # collection "Discover podcasts"
        items = list(self.run_callback(menu.list_container_content, urn=f'urn:bbc:radio:collection:{col_id}'))
        self.assertGreater(len(items), 6)


@patch('resources.lib.search.SearchHistory.update_last_used')
class Search(fixtures.WebTestCase):
    def test_search_results(self, _):
        argv = self.create_argv('search', 'do_search', keyword='smiths')
        self.run_addon(argv, items_count=20)

    def test_search_without_results(self, _):
        argv = self.create_argv('search', 'do_search', keyword='blablabla')
        self.run_addon(argv, items_count=0)


class PlayStream(fixtures.WebTestCase):
    def test_play_live_omega(self):
        self.kodi_version = '21'
        item = self.run_callback(stream.play_live, service_id='bbc_radio_one')
        self.assertIsInstance(item, fixtures.ListItemMock)
        self.assertTrue('.mpd' in item.getPath())
        self.assertFalse('m3u8' in item.getPath())

    def test_play_live_piers_beta(self):
        self.kodi_version = '22'
        item = self.run_callback(stream.play_live, service_id='bbc_radio_one')
        self.assertIsInstance(item, fixtures.ListItemMock)
        self.assertFalse('.mpd' in item.getPath())
        self.assertTrue('m3u8' in item.getPath())
