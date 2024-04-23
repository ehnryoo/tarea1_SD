Tarea 1 - Sistemas Distribuidos, 1-2024
Ernesto Villa y Cristóbal Barra


git clone https://github.com/ehnryoo/tarea1_SD

cd tarea1_SD

sudo docker-compose up --build 

--------------SERVER CACHE CLASICO-----------------
docker-compose up -d cache-server-classic
docker-compose stop -d cache-server-classic

--------------SERVER CACHE PARTICIONADO-----------------
docker-compose up -d cache-server-partitioned
docker-compose stop cache-server-partitioned

--------------SERVER CACHE CLASICO-----------------
docker-compose up -d cache-server-replicated
docker-compose stop -d cache-server-replicated

sudo docker-compose exec cache-server-classic python tests/test.py
