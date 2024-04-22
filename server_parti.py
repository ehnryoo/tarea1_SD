# server.py

import grpc
import time
import requests
from concurrent import futures
import cache_pb2
import cache_pb2_grpc
import redis

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
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

class PartitionedCacheService(cache_pb2_grpc.CacheServiceServicer):
    def __init__(self):
        self.redis_cache = RedisCache()

    def save_character_data(self, character_id, data):
        # Guardar datos en Redis con partición por ID
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
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cache_pb2_grpc.add_CacheServiceServicer_to_server(PartitionedCacheService(), server)
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
