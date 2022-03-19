# How to run Starwars API server using Docker

Open the command line shell and go to the root directory of the starwars-api repository.

Build the Docker image for the API server

```bash
docker build -t starwars-api:latest .
```

To run API server only, use the following command:

```bash
docker run --name starwars-api -d starwars-api:latest
```

To run API, MYSQL, and REDIS servers together in one shot, use the following command

```bash
docker-compose up -d
```

To turn down the servers, use the following command

```bash
docker-compose down
```
