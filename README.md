# Bank API

Bank API built in Python using FastAPI, Docker, Postgres and Rabbitmq


## Build and Run the images

```sh
docker-compose up -d
```

## Run the tests locally

```sh
docker-compose exec api python -m pytest
```

## Swagger Interface(OpenAPI)
```
http://localhost:80/docs/
```

## adminer Interface(DB visualization)
```
http://localhost:8080
```