## Basics
```bash
docker --version
docker info
docker ps                  # running containers
docker ps -a               # all containers
docker images
```

## Containers
```bash
docker run nginx
docker run -d nginx                          # detached
docker run --name mycontainer nginx          # custom name
docker run -p 8000:80 nginx                  # host:container port
docker run -v $(pwd):/app image_name         # bind mount (dev)

docker stop container_name
docker start container_name
docker restart container_name
docker rm container_name
docker container prune                       # remove all stopped
```

## Images
```bash
docker pull postgres
docker build -t image_name .                 # build from Dockerfile
docker tag image_name username/image_name:v1
docker rmi image_name
docker image prune                           # remove unused
```

## Volumes
```bash
docker volume ls
docker volume create postgres_data
docker volume inspect postgres_data
docker volume rm postgres_data
```

## Networks
```bash
docker network ls
docker network create my-network
docker network connect my-network container_name
docker network inspect my-network
docker network rm my-network
```

## Logs & Debugging
```bash
docker logs container_name
docker logs -f container_name                # follow live
docker exec -it container_name bash
docker top container_name
docker inspect container_name
docker cp file.txt container_name:/path/     # copy files
```

## Docker Compose
```bash
docker compose up
docker compose up -d                         # detached
docker compose up --build                    # rebuild
docker compose down
```

## Cleanup
```bash
docker system prune                          # containers, images, networks
docker system prune -a                       # aggressive
```

---

## PostgreSQL Container
```bash
docker run \
  --name fintrack-db \
  -v postgres_data:/var/lib/postgresql/data \
  -e POSTGRES_USER=your_username \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=finance_db \
  -p 5432:5432 \
  -d postgres

docker exec -it fintrack-db psql -U your_username
```

## FastAPI Connection Strings
```bash
# FastAPI on host → PostgreSQL in Docker
DATABASE_URL = "postgresql://user:pass@localhost:5432/finance_db"

# FastAPI in Docker → PostgreSQL in Docker (same network)
DATABASE_URL = "postgresql://user:pass@fintrack-db:5432/finance_db"
```

## Basic FastAPI Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Misc
```bash
lsof -i :5432                               # check who's using a port
```