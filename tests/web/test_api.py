# ------------------------------------------------------------------------------
#  Copyright (c) 2026 Dimitri Kroon.
#  This file is part of plugin.audio.bbcsounds.
#  SPDX-License-Identifier: GPL-3.0-or-later
#  See LICENSE.txt or https://www.gnu.org/licenses/gpl-3.0.txt
# ------------------------------------------------------------------------------

from __future__ import annotations
from tests.support import fixtures
fixtures.global_setup()

import re
import json
from unittest import TestCase
from datetime import datetime

import requests

from resources.lib import fetch

from support.object_checks import is_not_empty
from support.testutils import save_json, save_doc
from tests.support.object_checks import (
    has_keys,
    is_url
)


setUpModule = fixtures.setup_web_test


def scrape_sound_data(html):
    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.DOTALL)
    if not match:
        raise ValueError("HTML contains no __NEXT_DATA__ script tag.")
    data = json.loads(match[1])
    return data


def check_rail(testcase: TestCase, rail, obj_name: str):
    if rail['type'] == 'inline_header_module':
        return False
    has_keys(rail, 'type', 'id', 'title', 'description', 'state', 'uris', 'controls', 'data', obj_name=obj_name)
    testcase.assertTrue(rail['type'] in ('inline_display_module', ))
    testcase.assertTrue(is_not_empty(rail['title'], str))
    testcase.assertTrue(is_not_empty(rail['description'], str) or rail['description'] is None)
    if rail['uris'] is not None:
        testcase.assertIsInstance(rail['uris'], dict)
        testcase.assertEqual(len(rail['uris']), 2)          # Just to flag when more come up
        for key in rail['uris'].keys():
            testcase.assertTrue(key in ('pagination', 'polling'))
    if rail['controls'] is not None:
        testcase.assertIsInstance(rail['controls'], dict)
        for k, v in rail['controls'].items():
            testcase.assertTrue(k in ('sorting', 'navigation', 'context'))
            if k == 'navigation':
                has_keys(v, 'id', 'urn', 'title', 'target')
    testcase.assertIsInstance(rail['data'], list)
    return True


def check_playable_item(testcase: TestCase, item: dict, obj_name: str):
    testcase.assertEqual(item['type'], 'playable_item')
    has_keys(item, 'type', 'id', 'titles', 'synopses', 'image_url', 'duration', 'progress', 'download',
             'release', 'guidance', obj_name=obj_name)
    has_keys(item['titles'], 'primary', 'secondary', 'tertiary', 'entity_title', obj_name=obj_name + '.titles')
    has_keys(item['synopses'], 'long', 'medium', 'short', obj_name=obj_name + '.synopses')
    testcase.assertTrue(is_url(item['image_url'], ('.jpg', '.png')))
    has_keys(item['duration'], 'label', 'value', obj_name=obj_name + '.duration')
    if item['progress'] is not None:
        has_keys(item['progress'], 'label', 'value', obj_name=obj_name + '.progress')
        testcase.assertTrue(is_not_empty(item['progress']['value'], int))
    has_keys(item['availability'], 'from', 'label', 'to', obj_name=obj_name + '.availability')
    has_keys(item['release'], 'label', 'date', obj_name=obj_name + '.release')
    if item['download'] is not None:
        has_keys(item['download'], 'type', 'quality_variants', obj_name=obj_name + '.download')
    testcase.assertEqual(len(item), 18)
    if 'network' in item['urn']:
        check_live_item(testcase, item, obj_name=obj_name)


def check_live_item(testcase: TestCase, item: dict, obj_name: str):
    prgrm_time = item['titles']['secondary']
    start_t, end_t = prgrm_time.split(' - ')
    parsed_start_t = datetime.strptime(start_t, '%H:%M')
    parsed_end_t = datetime.strptime(end_t, '%H:%M')
    start_date = item['titles']['tertiary']
    parsed_start_date = datetime.strptime(start_date, '%d/%m/%Y')


def check_container_item(testcase: TestCase, item: dict, obj_name: str):
    testcase.assertEqual(item['type'], 'container_item')
    has_keys(item, 'type', 'id', 'urn', 'tlec_urn', 'titles', 'synopses', 'image_url', 'uris',
             'playable_count', obj_name=obj_name)
    has_keys(item['titles'], 'primary', 'secondary', 'tertiary', obj_name=obj_name + '.titles')
    if item['synopses'] is not None:
        has_keys(item['synopses'], 'long', 'medium', 'short', obj_name=obj_name + '.synopses')
    testcase.assertTrue(is_url(item['image_url'], ('.jpg', '.png')))
    check_uris(testcase, item['uris'], obj_name)


def check_uris(testcase: TestCase, uris: list | None, obj_name):
    if uris is None:
        return
    testcase.assertIsInstance(uris, list)
    for uri in uris:
        has_keys(uri, 'type', 'label', 'uri', obj_name=obj_name + '.uris')
        testcase.assertTrue(uri['type'] in ('latest', 'popular'))
        testcase.assertFalse(is_url(uri['uri']))  # is just the callb_path, without protocol and domain.


class WebPage(TestCase):
    def check_page(self, url, obj_name: str):
        resp = fetch.get(url)
        # save_doc(resp.text, 'homepage.html')
        data = scrape_sound_data(resp.text)
        # save_json(data, 'homepage.json')
        rails = data['props']['pageProps']['dehydratedState']['queries'][1]['state']['data']['data']
        for rail in rails:
            obj_name = obj_name + '/rail_' + rail['title']
            if check_rail(self, rail, obj_name) is False:
                continue
            if not rail['data']:
                continue
            for prgrm in rail['data']:
                prgrm_type = prgrm['type']
                if prgrm_type == 'playable_item':
                    check_playable_item(self, prgrm, obj_name + '/' + prgrm['titles']['primary'])
                elif prgrm_type == 'container_item':
                    check_container_item(self, prgrm, obj_name + '/' + prgrm['titles']['primary'])

    def test_home_page(self):
        self.check_page('https://www.bbc.co.uk/sounds', 'home-page')

    def test_music_page(self):
        self.check_page('https://www.bbc.co.uk/sounds/music', 'music-page')

    def test_podcast_page(self):
        self.check_page('https://www.bbc.co.uk/sounds/podcasts', 'podcasts-page')

    def test_mysounds_page(self):
        self.check_page('https://www.bbc.co.uk/sounds/podcasts', 'mysounds-page')


class LiveStationsPages(TestCase):
    def test_all_live_stations(self):
        url = 'https://www.bbc.co.uk/sounds/stations'
        resp = requests.get(url)
        data = scrape_sound_data(resp.text)
        # NOTE: this response has only 1 query!
        rails = data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']
        for rail in rails:
            check_rail(self, rail, obj_name=f'live_stations_{rail["id"]}')
            for station in rail['data']:
                check_live_item(self, station, obj_name=f'{rail["id"]}_{station["id"]}')



class BrandPage(TestCase):
    # Brand The archers; 6 pages of 29 episodes
    brand_id = 'b006qpgr'

    def test_get_multipage_episodes_default_page(self):
        resp = requests.get(f'https://www.bbc.co.uk/sounds/brand/{self.brand_id}')
        data = scrape_sound_data(resp.text)
        page_items = data['props']['pageProps']['dehydratedState']['queries'][1]['state']['data']['data']

        header = page_items[0]
        self.assertEqual(header['type'], 'inline_header_module')
        self.assertEqual(header['id'], 'container')
        self.assertEqual(header['data']['id'], self.brand_id)

        items_container = page_items[1]
        self.assertEqual(items_container['type'], 'inline_display_module')
        self.assertEqual(items_container['id'], 'container_list')
        for item in items_container['data']:
            check_playable_item(self, item, obj_name=f'brand_{self.brand_id}')

        pagination = items_container['uris']['pagination']
        self.assertEqual(pagination['total'], items_container['total'])
        self.assertEqual(pagination['limit'], 30)


class CategoryPage(TestCase):
    def test_category_sienceandtechnology(self):
        resp = requests.get('https://www.bbc.co.uk/sounds/category/factual-scienceandnature-scienceandtechnology?sort=latest')
        data = scrape_sound_data(resp.text)
        page_items = data['props']['pageProps']['dehydratedState']['queries'][1]['state']['data']['data']

        header = page_items[0]
        self.assertEqual(header['type'], 'inline_header_module')
        self.assertEqual(header['id'], 'category')

        items_container = page_items[1]
        self.assertEqual(items_container['type'], 'inline_display_module')
        self.assertEqual(items_container['id'], 'container_list')
        for item in items_container['data']:
            check_playable_item(self, item, obj_name='category-content')

        pagination = items_container['uris']['pagination']
        self.assertEqual(pagination['total'], items_container['total'])
        self.assertEqual(pagination['limit'], 30)
        self.assertTrue(pagination['uri'].startswith('/v2/programmes/'))

        controls = items_container['controls']
        self.assertIsInstance(controls, dict)
        for control in controls.values():
            if control is None:
                continue
            self.assertTrue(is_not_empty(control['id'], str))
            self.assertTrue(is_not_empty(control['urn'], str))


class RmsApi(TestCase):
    # Brand The archers; 6 pages of 29 episodes
    # brand_id = 'b006qpgr'
    #
    brand_id = 'p0ftp7pt'

    def test_brand_from_rms(self):
        url = f'https://rms.api.bbc.co.uk/v2/programmes/playable?container={self.brand_id}&sort=sequential&type=episode&experience=domestic&offset=0&limit=1000'
        resp = requests.get(url)
        data = resp.json()
        self.assertEqual(data['limit'], 1000)
        self.assertGreater(data['total'], 150)      # The Archers had 170 episode available at the time of developing.
        items_list = data['data']
        self.assertIsInstance(items_list, list)
        self.assertEqual(len(items_list), data['total'])
        for item in items_list:
            check_playable_item(self, item, f'brand_{self.brand_id}')


class Collections(TestCase):
    coll_id = 'm002ysc6'        # South Asian Heritage
    dflt_params = {'experience': 'domestic', 'offset': 0, 'limit': 1000}

    def test_get_all_collection_members(self):
        """Collection returning both container and playable items."""
        url = f'https://rms.api.bbc.co.uk/v2/collections/{self.coll_id}/members'
        resp = requests.get(url, params=self.dflt_params)
        data = resp.json()
        self.assertEqual(data['limit'], 1000)
        self.assertGreater(data['total'], 30)
        brand_ids = set()
        # collect all brand IDs in the collection
        brand_ids = {item['id'] for item in data['data'] if item['type'] == 'container_item'}
        self.assertGreater(len(brand_ids) , 10)
        # Check if playable items in the collection already have their brand listed.
        playable_brand_ids = set()
        for item in data['data']:
            if item['type'] == 'playable_item':
                self.assertTrue(item['container']['type'] in ('brand', 'series'))
                playable_brand_ids.add(item['container']['id'])

        playables_in_brands = brand_ids.intersection(playable_brand_ids)
        # Most playables do not have their brand already listed
        self.assertNotEqual(len(playables_in_brands), len(playable_brand_ids))
        # but some do
        self.assertTrue(len(playables_in_brands) > 0)
        return brand_ids, playable_brand_ids

    def test_compare_containers_member_types(self):
        # Get all members
        url = f'https://rms.api.bbc.co.uk/v2/collections/{self.coll_id}/members'
        resp = requests.get(url, params=self.dflt_params)
        members_list = resp.json()['data']
        playable_members = [item for item in members_list if item['type'] == 'playable_item']
        container_members = [item for item in members_list if item['type'] == 'container_item']

        # Get container members only
        url = f'https://rms.api.bbc.co.uk/v2/collections/{self.coll_id}/members/container'
        resp = requests.get(url, params=self.dflt_params)
        container_list = resp.json()['data']
        self.assertListEqual(container_list, container_members)

        # Get playable members only
        url = f'https://rms.api.bbc.co.uk/v2/collections/{self.coll_id}/members/playable'
        resp = requests.get(url, params=self.dflt_params)
        playable_list = resp.json()['data']
        self.assertListEqual(playable_list, playable_members)

    def test_collection_sorting(self):
        """The sort argument does not seem to have any effect; the lists are returned in the same
        unsorted order.

        """
        params = self.dflt_params.copy()
        url = f'https://rms.api.bbc.co.uk/v2/collections/{self.coll_id}/members'
        unsorted = requests.get(url, params=self.dflt_params).json()['data']
        params['sort'] = 'sequential'
        sequencial = requests.get(url, params=params).json()['data']
        params['sort'] = 'az'
        az = requests.get(url, params=params).json()['data']
        params['sort'] = 'popular'
        popular = requests.get(url, params=params).json()['data']

        self.assertEqual(unsorted, sequencial)
        self.assertEqual(unsorted, az)
        self.assertEqual(unsorted, popular)
