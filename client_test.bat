@echo off

curl -X POST -H "Content-Type: application/json" -d "{\"num_of_projects\":25}" http://127.0.0.1:8081/github/requests

echo Project: Django
curl http://127.0.0.1:8081/github/projects/django/django

echo Project: Real-Time-Voice-Cloning
curl http://127.0.0.1:8081/github/projects/CorentinJ/Real-Time-Voice-Cloning

echo Package: requests
curl http://127.0.0.1:8081/github/packages/requests

pause
