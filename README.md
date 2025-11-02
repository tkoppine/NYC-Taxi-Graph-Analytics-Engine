# NYC Taxi Graph Analytics Engine

A high-performance graph analytics engine for processing and analyzing New York City taxi trip data using Neo4j graph database, featuring advanced graph algorithms and containerized deployment capabilities.

## 🎯 Overview

This project implements a robust NYC taxi graph analytics engine that:

- **Loads and transforms** NYC Yellow Taxi trip data from Parquet format into Neo4j graph database
- **Creates graph relationships** between pickup and dropoff locations in the Bronx area
- **Implements graph algorithms** including Breadth-First Search (BFS) and PageRank
- **Provides containerized deployment** with Docker and Kubernetes support
- **Includes comprehensive testing** to validate data loading and algorithm implementations

## 🏗️ Architecture

```
NYC-Taxi-Graph-Analytics-Engine/
├── src/                    # Source code
│   ├── data_loader.py     # Data ingestion and transformation
│   └── interface.py       # Graph algorithms interface
├── tests/                 # Test suite
│   └── tester.py         # Comprehensive testing framework
├── deployment/           # Deployment configurations
│   ├── docker/          # Docker configuration
│   │   └── Dockerfile   # Container definition
│   └── kubernetes/      # Kubernetes manifests
│       ├── kafka-setup.yaml
│       ├── kafka-neo4j-connector.yaml
│       ├── neo4j-values.yaml
│       └── zookeeper-setup.yaml
├── docs/                # Documentation
└── requirements.txt     # Python dependencies
```

## 🚀 Features

### Data Processing

- **Parquet to Graph Transformation**: Efficiently loads NYC taxi trip data
- **Data Filtering**: Focuses on Bronx area trips with quality filters
- **Graph Modeling**: Creates Location nodes with Trip relationships

### Graph Algorithms

- **Breadth-First Search (BFS)**: Find shortest paths between locations
- **PageRank**: Identify most important/central locations in the network
- **Graph Data Science (GDS)**: Leverages Neo4j's built-in graph algorithms

### Deployment Options

- **Docker**: Containerized deployment with Neo4j and dependencies
- **Kubernetes**: Scalable orchestration with Kafka integration
- **Local Development**: Direct Python execution for development

## 📋 Prerequisites

- Python 3.8+
- Neo4j 5.5.0+
- Docker (for containerized deployment)
- Kubernetes (for orchestrated deployment)

## 🛠️ Installation

### Local Development Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/tkoppine/NYC-Taxi-Graph-Analytics-Engine.git
   cd NYC-Taxi-Graph-Analytics-Engine
   ```

2. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Neo4j**

   - Install Neo4j 5.5.0
   - Install Graph Data Science plugin
   - Configure authentication

4. **Configure environment variables**

   ```bash
   cp .env.example .env
   # Edit .env file and replace YOUR_NEO4J_PASSWORD with your actual Neo4j password
   ```

5. **Update password in source files**
   - Replace `YOUR_NEO4J_PASSWORD` in `src/data_loader.py`
   - Replace `YOUR_NEO4J_PASSWORD` in `tests/tester.py`

### Docker Deployment

⚠️ **Before deploying, update the following:**

- Replace `YOUR_NEO4J_PASSWORD` in `deployment/docker/Dockerfile`
- Replace `YOUR_ACCESS_TOKEN@github.com/YOUR_USERNAME/YOUR_REPO.git` with your repository details

1. **Build the container**

   ```bash
   cd deployment/docker
   docker build -t nyc-taxi-analytics .
   ```

2. **Run the container**
   ```bash
   docker run -p 7474:7474 -p 7687:7687 nyc-taxi-analytics
   ```

### Kubernetes Deployment

⚠️ **Before deploying, update the following:**

- Replace `YOUR_NEO4J_PASSWORD` in `deployment/kubernetes/neo4j-values.yaml`

1. **Deploy infrastructure components**

   ```bash
   kubectl apply -f deployment/kubernetes/zookeeper-setup.yaml
   kubectl apply -f deployment/kubernetes/kafka-setup.yaml
   ```

2. **Deploy Neo4j**
   ```bash
   helm repo add neo4j https://helm.neo4j.com/neo4j
   helm install neo4j neo4j/neo4j -f deployment/kubernetes/neo4j-values.yaml
   ```

## 🎮 Usage

### Data Loading

```python
from src.data_loader import DataLoader

# Initialize connection
loader = DataLoader("neo4j://localhost:7687", "neo4j", "password")

# Load and transform data
loader.load_transform_file("yellow_tripdata_2022-03.parquet")

# Close connection
loader.close()
```

### Graph Algorithms

```python
from src.interface import Interface

# Initialize interface
interface = Interface("neo4j://localhost:7687", "neo4j", "password")

# Find shortest path between locations
path = interface.bfs(start_node=159, last_node=212)

# Calculate PageRank scores
rankings = interface.pagerank(max_iterations=20, weight_property="distance")

# Close connection
interface.close()
```

### Running Tests

```bash
python tests/tester.py
```

## 📊 Data Model

### Nodes

- **Location**: Represents taxi zone locations in the Bronx
  - Properties: `name` (zone ID)

### Relationships

- **TRIP**: Connects pickup and dropoff locations
  - Properties: `distance`, `fare`, `pickup_dt`, `dropoff_dt`

### Graph Structure

```
(Location {name: 159})-[:TRIP {distance: 2.5, fare: 12.0}]->(Location {name: 212})
```

## 🧪 Testing

The test suite validates:

- **Data Loading**: Verifies correct number of nodes and relationships
- **BFS Algorithm**: Tests pathfinding between specific locations
- **PageRank Algorithm**: Validates centrality calculations

Expected test results:

- Nodes: 42 (Bronx locations)
- Relationships: 1,530 (filtered trips)
- PageRank: Location 159 should have highest score (~3.228)

## 🔧 Configuration

### Neo4j Configuration

- Default password: Update in all configuration files
- GDS Plugin: Required for graph algorithms
- Memory allocation: 2GB recommended

### Data Filtering

- Geographic scope: Bronx taxi zones only
- Quality filters: Trip distance > 0.1 miles, fare > $2.50

## 📈 Performance Considerations

- **Memory**: Neo4j requires adequate heap size for graph operations
- **Storage**: 2GB minimum for data and indexes
- **Network**: Ensure proper port configuration (7474, 7687)

## 🆘 Troubleshooting

### Common Issues

1. **Connection Timeout**: Ensure Neo4j is running and accessible
2. **Memory Errors**: Increase Neo4j heap size
3. **Authentication Failures**: Verify credentials in configuration files
4. **Missing Data**: Ensure parquet file is in the correct directory

### Support

For issues and questions:

- Check the [documentation](docs/)
- Review test output for specific error messages
- Verify all dependencies are installed correctly

## 📚 References

- [Neo4j Documentation](https://neo4j.com/docs/)
- [Graph Data Science Library](https://neo4j.com/docs/graph-data-science/)
- [NYC Taxi Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
