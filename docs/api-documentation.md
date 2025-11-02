# API Documentation

## Environment Configuration

⚠️ **Important**: Before using the API, make sure to update all password placeholders:

- Replace `YOUR_NEO4J_PASSWORD` with your actual Neo4j database password in all files
- Update environment variables in `.env` file (copy from `.env.example`)

## DataLoader Class

### Overview

The `DataLoader` class handles the ingestion and transformation of NYC taxi trip data from Parquet format into Neo4j graph database.

### Constructor

```python
DataLoader(uri, user, password)
```

**Parameters:**

- `uri` (str): URI of the Neo4j database (e.g., "neo4j://localhost:7687")
- `user` (str): Username for Neo4j authentication
- `password` (str): Password for Neo4j authentication

### Methods

#### `load_transform_file(file_path)`

Loads a parquet file, filters the data for Bronx trips, and creates graph nodes and relationships.

**Parameters:**

- `file_path` (str): Path to the parquet file to be processed

**Data Transformations:**

1. Filters for Bronx taxi zones only
2. Removes trips with distance ≤ 0.1 miles
3. Removes trips with fare ≤ $2.50
4. Converts datetime columns to proper format

**Graph Creation:**

- Creates Location nodes for each taxi zone
- Creates TRIP relationships with properties: distance, fare, pickup_dt, dropoff_dt

#### `close()`

Closes the Neo4j database connection.

---

## Interface Class

### Overview

The `Interface` class provides graph algorithm implementations using Neo4j's Graph Data Science library.

### Constructor

```python
Interface(uri, user, password)
```

**Parameters:**

- `uri` (str): URI of the Neo4j database
- `user` (str): Username for Neo4j authentication
- `password` (str): Password for Neo4j authentication

### Methods

#### `bfs(start_node, last_node)`

Performs Breadth-First Search to find paths between two locations.

**Parameters:**

- `start_node` (int): Starting location ID
- `last_node` (int): Target location ID

**Returns:**

- List of dictionaries containing path information
- Each path contains a list of nodes with their names

**Example:**

```python
interface = Interface("neo4j://localhost:7687", "neo4j", "password")
paths = interface.bfs(159, 212)
print(paths[0]['path'])  # [{'name': 159}, {'name': 212}]
```

#### `pagerank(max_iterations, weight_property)`

Calculates PageRank centrality scores for all locations in the graph.

**Parameters:**

- `max_iterations` (int): Maximum number of iterations for the algorithm
- `weight_property` (str): Edge property to use as weights ("distance" or "fare")

**Returns:**

- List containing two dictionaries: [max_pagerank, min_pagerank]
- Each dictionary contains 'name' and 'score' keys

**Example:**

```python
rankings = interface.pagerank(20, "distance")
print(f"Highest: {rankings[0]['name']} (score: {rankings[0]['score']})")
print(f"Lowest: {rankings[1]['name']} (score: {rankings[1]['score']})")
```

#### `close()`

Closes the Neo4j database connection.

---

## Graph Schema

### Nodes

**Location**

- `name` (int): Taxi zone ID

### Relationships

**TRIP**

- `distance` (float): Trip distance in miles
- `fare` (float): Trip fare amount in dollars
- `pickup_dt` (datetime): Pickup timestamp
- `dropoff_dt` (datetime): Dropoff timestamp

### Cypher Examples

**Create a location:**

```cypher
MERGE (l:Location {name: 159})
```

**Create a trip relationship:**

```cypher
MATCH (pickup:Location {name: 159}), (dropoff:Location {name: 212})
CREATE (pickup)-[:TRIP {
    distance: 2.5,
    fare: 12.0,
    pickup_dt: datetime('2022-03-01T10:30:00'),
    dropoff_dt: datetime('2022-03-01T10:45:00')
}]->(dropoff)
```

**Find all trips from a location:**

```cypher
MATCH (start:Location {name: 159})-[trip:TRIP]->(end:Location)
RETURN start, trip, end
```
