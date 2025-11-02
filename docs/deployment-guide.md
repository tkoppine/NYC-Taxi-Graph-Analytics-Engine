# Deployment Guide

⚠️ **Configuration Required**: Before deploying, you must update all password and repository placeholders:

- Replace `YOUR_NEO4J_PASSWORD` with your desired Neo4j password
- Replace `YOUR_ACCESS_TOKEN@github.com/YOUR_USERNAME/YOUR_REPO.git` with your repository URL
- Update all configuration files as detailed below

## Docker Deployment

### Prerequisites

- Docker installed and running
- At least 4GB RAM available
- Ports 7474 and 7687 available

### Building the Container

1. **Navigate to the docker directory:**

   ```bash
   cd deployment/docker
   ```

2. **Build the image:**

   ```bash
   docker build -t nyc-taxi-analytics .
   ```

3. **Run the container:**

   ```bash
   docker run -d \
     --name nyc-taxi-analytics \
     -p 7474:7474 \
     -p 7687:7687 \
     nyc-taxi-analytics
   ```

4. **Verify the deployment:**
   - Open http://localhost:7474 in your browser
   - Login with username: `neo4j`, password: `enter your pwd here`

### Container Details

The Docker container includes:

- Ubuntu 22.04 base image
- Neo4j 5.5.0 with Graph Data Science plugin
- Python 3 with required packages
- Pre-loaded NYC taxi trip data
- Automatic database initialization

---

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (local or cloud)
- kubectl configured
- Helm 3 installed
- At least 4GB RAM per node

### Step-by-Step Deployment

#### 1. Deploy Zookeeper

```bash
kubectl apply -f deployment/kubernetes/zookeeper-setup.yaml
```

#### 2. Deploy Kafka

```bash
kubectl apply -f deployment/kubernetes/kafka-setup.yaml
```

#### 3. Add Neo4j Helm Repository

```bash
helm repo add neo4j https://helm.neo4j.com/neo4j
helm repo update
```

#### 4. Deploy Neo4j

```bash
helm install neo4j neo4j/neo4j -f deployment/kubernetes/neo4j-values.yaml
```

#### 5. Deploy Kafka-Neo4j Connector (Optional)

```bash
kubectl apply -f deployment/kubernetes/kafka-neo4j-connector.yaml
```

### Verification

1. **Check pod status:**

   ```bash
   kubectl get pods
   ```

2. **Get Neo4j service details:**

   ```bash
   kubectl get svc neo4j
   ```

3. **Port forward to access Neo4j:**
   ```bash
   kubectl port-forward svc/neo4j 7474:7474 7687:7687
   ```

### Configuration Details

#### Neo4j Configuration (neo4j-values.yaml)

- **Resources**: 1 CPU, 2GB RAM
- **Storage**: 2GB persistent volume
- **Plugins**: Graph Data Science enabled
- **Security**: Custom password (update before deployment)

#### Kafka Configuration (kafka-setup.yaml)

- **Broker ID**: 1
- **External Port**: 9092
- **Internal Port**: 29092
- **Zookeeper**: Connected to zookeeper-service:2181

#### Resource Requirements

- **Neo4j**: 1 CPU, 2GB RAM, 2GB storage
- **Kafka**: 1 CPU, 1GB RAM
- **Zookeeper**: 0.5 CPU, 512MB RAM

---

## Local Development

### Prerequisites

- Python 3.8+
- Neo4j 5.5.0+ installed locally
- Graph Data Science plugin

### Setup Steps

1. **Install Neo4j:**

   - Download from https://neo4j.com/download/
   - Install Graph Data Science plugin
   - Start Neo4j service

2. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Neo4j:**

   - Set initial password
   - Enable GDS procedures in neo4j.conf:
     ```
     dbms.security.procedures.unrestricted=gds.*
     ```

4. **Run the application:**
   ```bash
   python src/data_loader.py
   python tests/tester.py
   ```

---

## Environment Variables

### Docker Environment

- `NEO4J_AUTH`: neo4j/enter your pwd here
- `NEO4J_PLUGINS`: ["graph-data-science"]
- `NEO4J_dbms_security_procedures_unrestricted`: gds.\*

### Kubernetes Environment

- Configured via neo4j-values.yaml
- Secrets for database passwords
- ConfigMaps for application settings

---

## Monitoring and Troubleshooting

### Health Checks

**Docker:**

```bash
docker logs nyc-taxi-analytics
docker exec -it nyc-taxi-analytics neo4j status
```

**Kubernetes:**

```bash
kubectl logs deployment/neo4j
kubectl describe pod <neo4j-pod-name>
```

### Common Issues

1. **Memory Issues**:

   - Increase container/pod memory limits
   - Adjust Neo4j heap size

2. **Port Conflicts**:

   - Check if ports 7474/7687 are available
   - Use different port mappings if needed

3. **Authentication Failures**:

   - Verify password configuration
   - Check Neo4j authentication settings

4. **Plugin Issues**:
   - Ensure GDS plugin is properly installed
   - Verify procedure whitelist configuration

### Performance Tuning

1. **Neo4j Memory Settings**:

   ```
   dbms.memory.heap.initial_size=1G
   dbms.memory.heap.max_size=1G
   dbms.memory.pagecache.size=512M
   ```

2. **Container Resources**:
   - Minimum 2GB RAM for Neo4j
   - SSD storage recommended
   - Adequate CPU for graph operations
