

class LRUCache:
def set(self, key: str, value: Any) -> None:
    # If key already exists, update and mark as used
    if key in self.cache:
        self.cache[key] = value
        self._mark_used(key)
        return

    # If cache is full, remove least recently used
    if len(self.order) >= self.capacity:
        lru_key = self.order.pop(0)
        del self.cache[lru_key]

    # Insert the new key
    self.cache[key] = value
    self._mark_used(key)