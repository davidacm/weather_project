#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from weather_project.app import cache_service


class FakeTime:
    def __init__(self) -> None:
        self.cur_time = 0

    def time(self):
        return self.cur_time

time = FakeTime()
cache_service.time = time
cache = cache_service.Cache(120)


class TestCache(unittest.TestCase):
    def test_cache(self):
        time.cur_time = 100
        cache.set('a', 'b')
        time.cur_time = 219
        self.assertIsNotNone(cache.get('a'))

    def test_expired_cache(self):
        time.cur_time = 100
        cache.set('b', 'c')
        time.cur_time = 221
        self.assertIsNone(cache.get('b'))

    def test_cache_cleaner(self):
        time.cur_time = 100
        # keys to be removed:
        cache.set('ra', 'a')
        cache.set('rb', 'b')

        time.cur_time += 60
        # keys that shouln't be removed.
        cache.set('na', 'a')
        cache.set('nb', 'a')

        time.cur_time = 221
        cache.clear_expired()
        self.assertIsNotNone(cache.get('na'))
        self.assertIsNotNone(cache.get('nb'))

        # to ensure removal was done, .get won't work here. Check the dict directly.
        self.assertNotIn('ra', cache._cache)
        self.assertNotIn('rb', cache._cache)
