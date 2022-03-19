# How to run Starwars API server using Docker

Open the command line shell and go to the root directory of the starwars-api repository.

Build the Docker image for the API server

```bash
docker build -t starwars-api:latest .
```

Run API, MYSQL, and REDIS servers with the following command

```bash
docker-compose up -d
```
