import grpc
import time
import requests
from concurrent import futures
import cache_pb2
import cache_pb2_grpc
import redis

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class RedisReplicatedCache:
    def __init__(self, master_host='localhost', master_port=6379, slave_host='localhost', slave_port=6380, db=0):
        self.master_cache = redis.StrictRedis(host=master_host, port=master_port, db=db, decode_responses=True)
        self.slave_cache = redis.StrictRedis(host=slave_host, port=slave_port, db=db, decode_responses=True)

    def is_redis_up(self):
        try:
            return self.master_cache.ping() and self.slave_cache.ping()
        except redis.ConnectionError:
            return False

    def get(self, key):
        return self.slave_cache.get(key) or self.master_cache.get(key)

    def set(self, key, value):
        self.master_cache.set(key, value)
        self.slave_cache.set(key, value)

class ReplicatedCacheService(cache_pb2_grpc.CacheServiceServicer):
    def __init__(self):
        self.redis_cache = RedisReplicatedCache()

    def save_character_data(self, character_id, data):
        self.redis_cache.set(f"character:{character_id}", data)

    def get_character_data(self, character_id):
        character_url = f"https://rickandmortyapi.com/api/character/{character_id}"
        response = requests.get(character_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def GetCharacterById(self, request, context):
        character_id = request.character_id
        cached_data = self.redis_cache.get(f"character:{character_id}")

        if cached_data:
            character_response = cache_pb2.CharacterResponse.FromString(cached_data)
            return character_response
        else:
            character_data = self.get_character_data(character_id)
            if character_data:
                character_response = cache_pb2.CharacterResponse(
                    name=character_data["name"],
                    status=character_data["status"],
                    species=character_data["species"],
                    type=character_data["type"],
                    gender=character_data["gender"]
                )
                self.save_character_data(character_id, character_response.SerializeToString())
                return character_response
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Character with ID {character_id} not found.")
                return cache_pb2.CharacterResponse()

def serve():
    redis_cache = RedisReplicatedCache()
    
    if not redis_cache.is_redis_up():
        print("¡Error! Los servidores Redis no están disponibles.")
        return
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cache_pb2_grpc.add_CacheServiceServicer_to_server(ReplicatedCacheService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("El servidor gRPC está en funcionamiento y escuchando en el puerto 50051.")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

