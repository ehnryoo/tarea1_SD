import redis

class CacheClient:
    def __init__(self, cache_type, *args, **kwargs):
        if cache_type == "redis":
            self.cache = RedisCache(*args, **kwargs)
        elif cache_type == "classic":
            self.cache = ClassicCache(*args, **kwargs)
        elif cache_type == "replicated":
            self.cache = ReplicatedCache(*args, **kwargs)
        elif cache_type == "partitioned":
            self.cache = PartitionedCache(*args, **kwargs)
        else:
            raise ValueError("Invalid cache type")

    def add_data(self, key, value):
        self.cache.add_data(key, value)

    def get_data(self, key):
        return self.cache.get_data(key)

    def print_cache(self):
        self.cache.print_cache()

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db)
        try:
            # Verificar la conexión con Redis
            self.redis_client.ping()
            print("Redis is up and running!")
        except redis.exceptions.ConnectionError:
            print("Unable to connect to Redis. Please make sure it's running.")

    def get(self, key):
        return self.redis_client.get(key)

    def set(self, key, value):
        self.redis_client.set(key, value)

class ClassicCache:
    def __init__(self, capacity):
        self.lru_cache = LRUCache(capacity)
        self.fifo_cache = FIFOCache(capacity)

    def get_data(self, key):
        return self.lru_cache.get(key), self.fifo_cache.get(key)

    def add_data(self, key, value):
        self.lru_cache.put(key, value)
        self.fifo_cache.put(key, value)

    def print_cache(self):
        self.lru_cache.print_cache()
        self.fifo_cache.print_cache()

class ReplicatedCache:
    def __init__(self, replicas, capacity_per_replica):
        self.replicas = replicas
        self.capacity_per_replica = capacity_per_replica
        self.lru_caches = [LRUCache(capacity_per_replica) for _ in range(replicas)]
        self.fifo_caches = [FIFOCache(capacity_per_replica) for _ in range(replicas)]

    def get_data(self, key):
        lru_data, fifo_data = None, None
        for lru_cache, fifo_cache in zip(self.lru_caches, self.fifo_caches):
            lru_data = lru_cache.get(key)
            fifo_data = fifo_cache.get(key)
            if lru_data and fifo_data:
                break
        return lru_data, fifo_data

    def add_data(self, key, value):
        for lru_cache, fifo_cache in zip(self.lru_caches, self.fifo_caches):
            lru_cache.put(key, value)
            fifo_cache.put(key, value)

    def print_cache(self):
        print("Replicated Cache:")
        for i, (lru_cache, fifo_cache) in enumerate(zip(self.lru_caches, self.fifo_caches)):
            print(f"Replica {i}:")
            lru_cache.print_cache()
            fifo_cache.print_cache()

class PartitionedCache:
    def __init__(self, partitions, capacity_per_partition):
        self.partitions = partitions
        self.capacity_per_partition = capacity_per_partition
        self.lru_caches = [LRUCache(capacity_per_partition) for _ in range(partitions)]
        self.fifo_caches = [FIFOCache(capacity_per_partition) for _ in range(partitions)]

    def hash_key(self, key):
        return hash(key) % self.partitions

    def get_data(self, key):
        partition = self.hash_key(key)
        return self.lru_caches[partition].get(key), self.fifo_caches[partition].get(key)

    def add_data(self, key, value):
        partition = self.hash_key(key)
        self.lru_caches[partition].put(key, value)
        self.fifo_caches[partition].put(key, value)

    def print_cache(self):
        print("Partitioned Cache:")
        for i, (lru_cache, fifo_cache) in enumerate(zip(self.lru_caches, self.fifo_caches)):
            print(f"Partition {i}:")
            lru_cache.print_cache()
            fifo_cache.print_cache()

# Ejemplo de uso
if __name__ == "__main__":
    # Verificar la conexión con Redis
    RedisCache()

"""
    # Crear un cliente de caché clásico con capacidad 5
    classic_client = CacheClient("classic", 5)
    classic_client.add_data("key1", "value1")
    classic_client.add_data("key2", "value2")
    classic_client.print_cache()

    # Crear un cliente de caché replicado con 3 réplicas y capacidad por réplica 3
    replicated_client = CacheClient("replicated", 3, 3)
    replicated_client.add_data("key1", "value1")
    replicated_client.add_data("key2", "value2")
    replicated_client.print_cache()

    # Crear un cliente de caché particionado con 4 particiones y capacidad por partición 3
    partitioned_client = CacheClient("partitioned", 4, 3)
    partitioned_client.add_data("key1", "value1")
    partitioned_client.add_data("key2", "value2")
    partitioned_client.print_cache()
"""