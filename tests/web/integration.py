# ------------------------------------------------------------------------------
#  Copyright (c) 2026 Dimitri Kroon.
#  This file is part of plugin.audio.bbcsounds.
#  SPDX-License-Identifier: GPL-3.0-or-later
#  See LICENSE.txt or https://www.gnu.org/licenses/gpl-3.0.txt
# ------------------------------------------------------------------------------
from __future__ import annotations
from tests.support import fixtures
fixtures.global_setup()

from unittest import TestCase

from resources.lib import plugin
from resources.lib import menu


setUpModule = fixtures.setup_web_test


class TestPages(fixtures.AddonRunner):
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


class TestRail(fixtures.AddonRunner):
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
            self.run_callback(menu.list_rail,
                              callb_kwargs={'page_url': 'https://www.bbc.co.uk/sounds', 'rail_id': rail_id},
                              items_min=6)

    def test_music_page_hero_rail_content(self):
        argv = self.create_argv('menu', 'list_rail', page_url='https://www.bbc.co.uk/muscic', rail_id='music_hero')
        self.run_addon(argv, items_min=6)

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
            argv = self.create_argv('menu', 'list_rail', page_url='https://www.bbc.co.uk/sounds', rail_id=rail_id)
            self.run_addon(argv, items_min=6)


class ContainerContent(fixtures.AddonRunner):
    def test_news_summary_page(self, ):
        argv = self.create_argv('menu', 'list_container_content', urn='urn:bbc:radio:brand:p0ddbgqd')
        self.run_addon(argv, items_min=20)

    def test_series(self):
        self.run_callback(menu.list_container_content, callb_kwargs={'urn': 'urn:bbc:radio:series:m001rgzp'})


class Search(fixtures.AddonRunner):
    def test_search_results(self, p_req, _):
        argv = self.create_argv('search', 'do_search', keyword='smiths')
        self.run_addon(argv, items_count=20)

    def test_search_without_results(self, ):
        argv = self.create_argv('search', 'do_search', keyword='blablabla')
        self.run_addon(argv, items_count=0)


class TestLogin(TestCase):
    def test_login_with_password(self):
        addon = plugin.Plugin(['plugin://plugin.audio.bbcsounds/resources/lib/account/login_with_passw',
                             '-1',
                             '',
                             'resume:false'])
        addon.run()





