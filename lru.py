#!/usr/bin/env python3
from typing import Any, Optional

class LRUCache:
    """
    A Least Recently Used (LRU) cache keeps items until it reaches
    the item limit. When full, inserting a new item removes the
    least recently used one.

    Methods to implement:
        - has(key) : returns True/False
        - get(key) : returns value or None, marks as recently used
        - set(key, value) : inserts/updates item, evicts if needed
    """

    def __init__(self, item_limit: int):
        self.limit = item_limit
        self.cache = {}            # key -> value
        self.order = []            # tracks LRU order (left = oldest)

    def _mark_used(self, key: str):
        """Move the key to the end (most recently used)."""
        if key in self.order:
            self.order.remove(key)
        self.order.append(key)

    def has(self, key: str) -> bool:
        return key in self.cache

    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None
        self._mark_used(key)
        return self.cache[key]

    def set(self, key: str, value: Any):
        # If already exists → update and mark as used
        if key in self.cache:
            self.cache[key] = value
            self._mark_used(key)
            return

        # If full → evict least recently used (oldest)
        if len(self.cache) >= self.limit:
            lru_key = self.order.pop(0)   # remove oldest
            del self.cache[lru_key]

        # Insert new item
        self.cache[key] = value
        self._mark_used(key)
