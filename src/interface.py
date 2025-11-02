from neo4j import GraphDatabase

class Interface:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        self._driver.verify_connectivity()

    def close(self):
        self._driver.close()

    def bfs(self, start_node, last_node):
        # TODO: Implement this method
        with self._driver.session() as session:
            # checking whether locationgraph already exists or not
            check_func = session.run("""
                CALL gds.graph.exists('locationGraph')
                YIELD exists
            """)

            # dropping locationgraph if it was already exists
            if check_func.single()['exists']:
                cl = "CALL gds.graph.drop('locationGraph')"
                session.run(cl)

            # projecting the graph into memory
            session.run(""" 
                CALL gds.graph.project(
                    'locationGraph',
                    'Location',
                    { 
                        TRIP: {
                            type: 'TRIP',
                            properties: ['distance'],
                            orientation: 'NATURAL'
                        }
                    }
                )
            """)

            # getting the start_name and end_name
            getting_nodes = """
                MATCH (l:Location)
                WHERE l.name IN [$start_name, $end_name]
                RETURN id(l) AS internal_id, l.name AS name
            """
            internal_ids = session.run(getting_nodes, start_name=start_node, end_name=last_node)

            # mapping the nodes to internal IDs
            node_map = {}
            for record in internal_ids:
                node_map[record['name']] = record['internal_id']

            # storing internal ids
            start_node_id = node_map.get(start_node)
            last_node_id = node_map.get(last_node)

            # checking whether ids were found or not
            if start_node_id is None or last_node_id is None:
                raise ValueError("Start or last node not found in the graph.")
            
            # now use gds inbuilt function gds.bfs.stream to run bfs and find the path
            rslt = session.run("""  
                CALL gds.bfs.stream(
                    'locationGraph',
                    {
                        sourceNode: gds.util.asNode($start_node_id),  
                        targetNodes: [gds.util.asNode($last_node_id)]
                    }
                )
                YIELD path
                RETURN path
            """, start_node_id=start_node_id, last_node_id=last_node_id)

            # store the result
            paths = []
            for recd in rslt:
                path_nodes = [{'name': node['name']} for node in recd['path'].nodes]
                paths.append({'path': path_nodes})

            # drop the locationgraph
            cl1 = "CALL gds.graph.drop('locationGraph')"
            session.run(cl1)
            return paths

    def pagerank(self, max_iterations, weight_property):
        # TODO: Implement this method
        with self._driver.session() as session:
            # checking whether locationgraph already exists or not
            check_func = session.run("""
                CALL gds.graph.exists('locationGraph')
                YIELD exists
            """)

            # dropping locationgraph if it was already exists
            if check_func.single()['exists']:
                cl2 = "CALL gds.graph.drop('locationGraph')"
                session.run(cl2)  

            # project the graph and give weight_property as properties
            session.run("""
                CALL gds.graph.project(
                    'locationGraph',
                    'Location',
                    { 
                        TRIP: {
                            type: 'TRIP',
                            properties: [$weight_property],
                            orientation: 'NATURAL'
                        }
                    }
                )
            """, weight_property=weight_property)

            # Using pageRank inbuilt function in gds to run the pagerank algorithm as below
            rslt = session.run("""
                CALL gds.pageRank.stream('locationGraph', {
                    maxIterations: $max_iterations,
                    dampingFactor: 0.85,
                    relationshipWeightProperty: $weight_property
                })
                YIELD nodeId, score
                RETURN gds.util.asNode(nodeId).name AS name, score
                ORDER BY score DESC
            """, max_iterations=max_iterations, weight_property=weight_property)
    
            # store the results 
            rslts_lst = []
            for recrd in rslt:
                rslts_lst.append({'name': recrd['name'], 'score': recrd['score']})

            # drop the locationGraph
            cl3 = "CALL gds.graph.drop('locationGraph')"
            session.run(cl3)

            # Finding maximum and minimum page rank and return them
            if rslts_lst:
                max_pag_rank = rslts_lst[0]
                min_pag_rank = rslts_lst[-1]
                return [max_pag_rank, min_pag_rank]
            
            return []
