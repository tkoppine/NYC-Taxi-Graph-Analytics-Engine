# Base image: ubuntu:22.04
FROM ubuntu:22.04

# ARGs
ARG TARGETPLATFORM=linux/amd64,linux/arm64
ARG DEBIAN_FRONTEND=noninteractive

# neo4j 5.5.0 installation and some cleanup
RUN apt-get update && \
    apt-get install -y wget gnupg software-properties-common git curl && \
    wget -O - https://debian.neo4j.com/neotechnology.gpg.key | apt-key add - && \
    echo 'deb https://debian.neo4j.com stable latest' > /etc/apt/sources.list.d/neo4j.list && \
    add-apt-repository universe && \
    apt-get update && \
    apt-get install -y nano unzip neo4j=1:5.5.0 python3 python3-pip openjdk-17-jdk && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Creating /cse511 (directory)
WORKDIR /cse511

# Downloading the dataset from trip-data into the /cse511 (directory)
RUN wget -O yellow_tripdata_2022-03.parquet https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-03.parquet

# Extracting the data_loader.py file from git hub to /cse511 (directory)
RUN git clone https://accesstokenkey@github.com/yourpath.git 

# First upgrade pip and later downloading neo4j pandas pyarrow
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install neo4j && \
    python3 -m pip install pyarrow pandas

# Installing Neo4j GDS plugin version 2.3.1 into /cse511 (directory)
RUN wget -O /var/lib/neo4j/plugins/neo4j-graph-data-science-2.3.1.jar https://github.com/neo4j/graph-data-science/releases/download/2.3.1/neo4j-graph-data-science-2.3.1.jar

# Using defual_listen_address to connect to localhost from any browser and for gds also connection established
RUN echo "dbms.default_listen_address=0.0.0.0" >> /etc/neo4j/neo4j.conf && \
    echo "dbms.security.auth_enabled=true" >> /etc/neo4j/neo4j.conf && \
    echo "dbms.security.procedures.unrestricted=gds.*" >> /etc/neo4j/neo4j.conf && \
    echo "dbms.security.procedures.allowlist=gds.*" >> /etc/neo4j/neo4j.conf

# Setting the default password for neo4j db
RUN neo4j-admin dbms set-initial-password enter your pwd here

# Run the data loader script
RUN chmod +x Project-1-tkoppine/data_loader.py && \
    neo4j start && \
    python3 Project-1-tkoppine/data_loader.py && \
    neo4j stop

# Expose neo4j ports
EXPOSE 7474 7687

CMD ["/bin/bash", "-c", "neo4j start && tail -f /dev/null"]
