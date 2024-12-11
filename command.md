pip freeze > requirements.txt
docker-compose up -d --build
docker exec -it django /bin/sh