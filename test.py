from flask import Flask, jsonify
import grpc
import cache_pb2
import cache_pb2_grpc
import redis

app = Flask(__name__)

# Configura la conexión a Redis
redis_host = 'localhost'
redis_port = 6379
cache = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

# Configura la conexión al servidor gRPC
channel = grpc.insecure_channel('localhost:50051')
stub = cache_pb2_grpc.CacheServiceStub(channel)

@app.route('/character-lru/<int:character_id>', methods=['GET'])
def get_character_info_lru(character_id):
    cached_data = cache.get(f"character:{character_id}")
    if cached_data:
        return jsonify({"name": cached_data})
    else:
        # Llama al servidor gRPC para obtener información del personaje
        request = cache_pb2.CharacterRequest(character_id=character_id)
        response = stub.GetCharacterById(request)
        if response.name:
            cache.set(f"character:{character_id}", response.name)  
            return jsonify({"name": response.name})
        else:
            return jsonify({"error": "Character not found"})

@app.route('/character-ttl/<int:character_id>', methods=['GET'])
def get_character_info_ttl(character_id):
    cached_data = cache.get(f"character:{character_id}")
    if cached_data:
        return jsonify({"name": cached_data})
    else:
        # Llama al servidor gRPC para obtener información del personaje
        request = cache_pb2.CharacterRequest(character_id=character_id)
        response = stub.GetCharacterById(request)
        if response.name:
            cache.setex(f"character:{character_id}", 3600, response.name)  # Expira en 1 hora
            return jsonify({"name": response.name})
        else:
            return jsonify({"error": "Character not found"})

if __name__ == '__main__':
    app.run(debug=True)

"""
from flask import Flask, jsonify
import grpc
import cache_pb2
import cache_pb2_grpc
import redis

app = Flask(__name__)

# Configuración de la conexión a Redis
redis_host = 'localhost'
redis_port = 6379
cache = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

# Configuración de la conexión al servidor gRPC
channel = grpc.insecure_channel('localhost:50051')
stub = cache_pb2_grpc.CacheServiceStub(channel)

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character_info(character_id):
    # Intenta recuperar los datos del personaje de la caché
    cached_data = cache.get(f"character:{character_id}")
    
    if cached_data:
        # Si los datos están en caché, devuelve la respuesta JSON
        return jsonify({"data": cached_data})
    else:
        # Si los datos no están en caché, llama al servidor gRPC para obtenerlos
        request = cache_pb2.CharacterRequest(character_id=character_id)
        response = stub.GetCharacterById(request)
        
        if response.name:
            # Si se encuentra el personaje, almacena los datos en caché y devuelve la respuesta JSON
            cache.set(f"character:{character_id}", response.name, ex=3600)  # Expira en 1 hora
            return jsonify({"data": response.name})
        else:
            # Si el personaje no se encuentra, devuelve un mensaje de error JSON
            return jsonify({"error": f"Character with ID {character_id} not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)
"""
"""
from flask import Flask, jsonify
import grpc
import cache_pb2
import cache_pb2_grpc
import redis

app = Flask(__name__)

# Configuración de la conexión a la instancia maestra de Redis
master_redis_host = 'localhost'
master_redis_port = 6379
master_cache = redis.StrictRedis(host=master_redis_host, port=master_redis_port, decode_responses=True)

# Configuración de la conexión a la instancia esclava de Redis
slave_redis_host = 'localhost'
slave_redis_port = 6380  # Puerto diferente para la instancia esclava
slave_cache = redis.StrictRedis(host=slave_redis_host, port=slave_redis_port, decode_responses=True)

# Configuración de la conexión al servidor gRPC
channel = grpc.insecure_channel('localhost:50051')
stub = cache_pb2_grpc.CacheServiceStub(channel)

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character_info(character_id):
    # Intenta recuperar los datos del personaje de la caché maestra
    cached_data = master_cache.get(f"character:{character_id}")
    
    if cached_data:
        # Si los datos están en caché, devuelve la respuesta JSON
        return jsonify({"data": cached_data})
    else:
        # Si los datos no están en caché, llama al servidor gRPC para obtenerlos
        request = cache_pb2.CharacterRequest(character_id=character_id)
        response = stub.GetCharacterById(request)
        
        if response.name:
            # Si se encuentra el personaje, almacena los datos en caché maestra y esclava
            master_cache.set(f"character:{character_id}", response.name, ex=3600)  # Expira en 1 hora
            slave_cache.set(f"character:{character_id}", response.name, ex=3600)  # Replica en la caché esclava
            return jsonify({"data": response.name})
        else:
            # Si el personaje no se encuentra, devuelve un mensaje de error JSON
            return jsonify({"error": f"Character with ID {character_id} not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)

"""
