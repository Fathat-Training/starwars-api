# To build:
# docker build -t starwars-api:latest .

FROM python:3.10.3

RUN mkdir -p /app/

COPY . /app/

WORKDIR /app/

# Install GCC (C compiler) to install certain Python requirements below.
RUN apt --yes update && \
    apt --yes install gcc && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

# No longer need GCC, uninstall it.
RUN apt --yes --purge remove gcc

RUN chmod +x run_server.sh

CMD ["./run_server.sh"]