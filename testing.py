import unittest
import requests
import time
import psutil
import matplotlib.pyplot as plt

class TestCacheServer(unittest.TestCase):
    base_url = "http://localhost:5000"

    def test_cache_lru_policy(self):
        character_ids = list(range(1, 30))  # IDs de personajes para probar
        response_times = []
        memory_usages = []

        for character_id in character_ids:
            # Realiza la consulta al servidor con la política de caché LRU
            start_time = time.time()
            response = requests.get(f"{self.base_url}/character-lru/{character_id}")
            end_time = time.time()

            # Registra el tiempo de respuesta en segundos
            elapsed_time = end_time - start_time
            response_times.append(elapsed_time)

            # Obtén la cantidad de memoria utilizada por el proceso actual
            process = psutil.Process()
            memory_usage = process.memory_info().rss / (1024 ** 2)  # Convertir a MB
            memory_usages.append(memory_usage)

            # Espera 0.1 segundo entre consultas
            time.sleep(0.1)

        # Genera el gráfico de dispersión
        plt.scatter(response_times, memory_usages)
        plt.xlabel('Tiempo de Respuesta (s)')
        plt.ylabel('Uso de Memoria (MB)')
        plt.title('Gráfico de Dispersión: Tiempo de Respuesta vs. Uso de Memoria')
        plt.grid(True)
        plt.show()

    def test_cache_ttl_policy(self):
        character_ids = list(range(1, 20))  # IDs de personajes para probar
        response_times = []
        memory_usages = []

        for character_id in character_ids:
            # Realiza la consulta al servidor con la política de caché TTL
            start_time = time.time()
            response = requests.get(f"{self.base_url}/character-ttl/{character_id}")
            end_time = time.time()

            # Registra el tiempo de respuesta en segundos
            elapsed_time = end_time - start_time
            response_times.append(elapsed_time)

            # Obtén la cantidad de memoria utilizada por el proceso actual
            process = psutil.Process()
            memory_usage = process.memory_info().rss / (1024 ** 2)  # Convertir a MB
            memory_usages.append(memory_usage)

            # Espera 0.1 segundo entre consultas
            time.sleep(0.1)

        # Genera el gráfico de dispersión
        plt.scatter(response_times, memory_usages)
        plt.xlabel('Tiempo de Respuesta (s)')
        plt.ylabel('Uso de Memoria (MB)')
        plt.title('Gráfico de Dispersión: Tiempo de Respuesta vs. Uso de Memoria')
        plt.grid(True)
        plt.show()

if __name__ == '__main__':
    unittest.main()
