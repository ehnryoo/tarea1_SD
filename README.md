git clone 
cd TAREA1-ERNESTOVILLA-CRISTOBALBARRA

docker-compose up --build 

docker-compose exec cache-server-classic python tests/test.py
