#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import threading
import time


class Cache:
    """a very basic cache implementation, you can use this to avoid frequent calls to an api.

    this is a temporal implementation, you can overwrite this with a specific service for better performance.
    """
    
    def __init__(self, expiration: int):
        """
        Args:
            expiration (int): the max time a (key, value) is valid, in seconds.
        """
        self.expiration = expiration
        self._cache = {}
        self.clean_is_running = False

    def set(self, key, value):
        self._cache[key] = (time.time(), value)

    def is_valid_key(self, key):
        return (time.time() - self.expiration) < self._cache[key][0]

    def get(self, key):
        if key not in self._cache or not self.is_valid_key(key):
            return None
        return self._cache[key][1]

    def clear_expired(self):
        """A method to clear the old stored keys."""
        remove_time = time.time() - self.expiration
        keys_to_remove = []
        for k, (val, _) in self._cache.items():
            if val < remove_time:
                keys_to_remove.append(k)
        for k in keys_to_remove:
            del self._cache[k]

    async def memory_task_cleaner(self, tick: int):
        """if this function is started, this method will clear the old keys each tick seconds. It's executed using asyncio.

        Args:
            tick (int): execution interval, in seconds.
        """
        if self.clean_is_running:
            return
        self.clean_is_running = True
        while True:
            await asyncio.sleep(tick)
            self.clear_expired()

    def thread_memory_task_cleaner(self, tick: int):
        """this method is intended to be used as a background thread, to clean the memory, without using asyncio but threads.
        Args:
            tick (int): time interval, in seconds.
        """
        if self.clean_is_running == True:
            return
        def background():
            self.clean_is_running = True
            while True:
                time.sleep(tick)
                self.clear_expired()
        bg = threading.Thread(target=background)
        bg.daemon = True
        bg.start()
