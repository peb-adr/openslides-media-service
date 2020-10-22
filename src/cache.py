class Cache:
    def __init__(self, database):
        self.database = database
        self.logger = database.logger

        self.lru_data = {}  # id <-> (data, mimetype)
        # ids in the order of access: lru_ids[0] has the oldest element
        self.lru_ids = []

        self.size = database.config["CACHE_SIZE"]
        self.data_min_size = database.config["CACHE_DATA_MIN_SIZE_KB"] * 1024
        self.data_max_size = database.config["CACHE_DATA_MAX_SIZE_KB"] * 1024
        self.logger.info(
            f"Init Cache (size={self.size} min_size_bytes={self.data_min_size} max_size_bytes={self.data_max_size})"
        )

    def get_mediafile(self, id):
        cache_data = self.lru_data.get(id)
        if cache_data is not None:
            self._refresh_id(id)
            self.logger.debug(f"Serve {id} from cache. Cache ids: {self.lru_ids}")
            return cache_data

        data, mimetype = self.database.get_mediafile(id)
        if len(data) <= self.data_max_size and len(data) >= self.data_min_size:
            self._cache(id, (data, mimetype))
            self.logger.debug(f"Put {id} into cache. Cache ids: {self.lru_ids}")
        else:
            self.logger.debug(
                f"{id} is not cached, since it is too small or large ({len(data)} bytes)"
            )

        return data, mimetype

    def shutdown(self):
        self.database.shutdown()

    def _cache(self, id, data):
        self._refresh_id(id)
        self.lru_data[id] = data

        while len(self.lru_ids) > self.size:
            removed_id = self.lru_ids.pop(0)  # remove first element
            del self.lru_data[removed_id]
            self.logger.debug(
                f"Cache full. Removed {removed_id} from cache. Cache ids: {self.lru_ids}"
            )

    def _remove_id(self, id):
        # Removes the id from lru_ids
        self.lru_ids = [_id for _id in self.lru_ids if _id != id]

    def _refresh_id(self, id):
        # appends the id at the end of lru_ids. Makes sure, the id is only there once.
        self._remove_id(id)
        self.lru_ids.append(id)
