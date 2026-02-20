import time
import hashlib
from collections import OrderedDict

from config import CACHE_MAX_SIZE, CACHE_TTL_SECONDS, EMBEDDING_SIM_THRESHOLD
from embeddings import embed, similarity

class CacheEntry:
    def __init__(self, answer, embedding):
        self.answer = answer
        self.embedding = embedding
        self.timestamp = time.time()

class Cache:
    def __init__(self):
        self.store = OrderedDict()

    def _hash(self, text: str):
        return hashlib.md5(text.encode()).hexdigest()

    def normalize(self, text: str):
        return text.strip().lower()

    def get_exact(self, query):
        key = self._hash(query)
        entry = self.store.get(key)

        if not entry:
            return None

        if time.time() - entry.timestamp > CACHE_TTL_SECONDS:
            del self.store[key]
            return None

        self.store.move_to_end(key)
        return entry.answer

    def get_semantic(self, query_embedding):
        for key, entry in self.store.items():
            if time.time() - entry.timestamp > CACHE_TTL_SECONDS:
                continue

            sim = similarity(query_embedding, entry.embedding)
            if sim >= EMBEDDING_SIM_THRESHOLD:
                self.store.move_to_end(key)
                return entry.answer

        return None

    def set(self, query, answer):
        emb = embed(query)
        self.set_with_embedding(query, answer, emb)

    def set_with_embedding(self, query, answer, embedding):
        if len(self.store) >= CACHE_MAX_SIZE:
            # Evict the oldest item (LRU)
            self.store.popitem(last=False)

        key = self._hash(query)
        self.store[key] = CacheEntry(answer, embedding)
        self.store.move_to_end(key)

cache = Cache()
