import warnings


class Graph(object):
    '''

        graph in the form
        {
            node = [[nodeA, weigh1], [nodeB, weigh2]],
            nodeA = [[nodeC, weigh3]]
        }
    '''

    def __init__(self, graph={}):
        '''
            sdfs
        '''
        self._graph = graph
        self._node_count = 0
        self._edge_count = 0

    @property
    def node_count(self):
        return self._node_count

    @property
    def edge_count(self):
        return self._edge_count

    def add_node(self, node):
        '''
            Adds node
            If it already exists, raise an Error
        '''
        if node not in self._graph:
            self._graph[node] = []
            self._node_count += 1
        else:
            raise ValueError("Node already exists in graph")

    def add_node_from(self, nodes):
        '''
            add nodes from list of nodes
            #TODO
        '''
        pass

    def add_edge(self, node_start, node_end, weight=1):
        '''
            Adds edge
            If weight is not specified, defaults to one
        '''

        # check if start node already exists
        if node_start not in self._graph:
            warnings.warn('The start node does not exist, adding it to graph', Warning)
            self.add_node(node_start)
            edges = self._graph[node_start]

        # check if edge already exists)
        for edge in edges:
            if edge[0] == node_end:
                raise ValueError("Edge already exiists")

        # check if end node already exists
        if node_end not in self._graph:
            warnings.warn('The end node does not exist, adding it to graph', Warning)
            self.add_node(node_end)

        self._graph[node_start].append([node_end, weight])
        self._edge_count += 1

    def delete_node(self, node):
        '''
            Removoes all node dependecnies and then removes node
        '''

        for key, values in self._graph.items():
            if key == node:
                for edge in values:
                    self._edge_count -= 1
                continue
            else:
                for edge in values:
                    if edge[0] == node:
                        self.delete_edge(key, node)

        self._graph.pop(node, None)
        self._node_count -= 1

    def delete_edge(self, node_start, node_end):

        if node_start not in self._graph:
            raise ValueError("The Start node does not exist")

        elif node_end not in self._graph:
            raise ValueError("The End node does not exist")

        edges = self._graph[node_start]
        for edge in edges:
            if edge[0] == node_end:
                self._graph[node_start].remove(edge)

        self._edge_count -= 1

    def delete_edge_from(self, node_start, node_end):
        # TODO
        pass

    def get_node_details(self, node):
        '''
            Returns all nodes connected to it in a dictionary
            dict = {
                node1: weigh1,
                node2: weigh2
            }
        '''
        if node in self._graph:
            temp_dict = {}
            edges = self._graph[node]

            for edge in edges:
                temp_dict[edge[0]] = edge[1]

            return temp_dict

        else:
            raise ValueError("Node does not exist")

    def update_edge(self, node_start, node_end, weight=None):
        '''
            Updates the weight of the edge
            if the new weight is not specified, it deletes that edge
        '''

        # check if nodes already exists
        if node_start not in self._graph:
            raise ValueError("The Start node does not exist")

        elif node_end not in self._graph:
            raise ValueError("The End node does not exist")

        if weight is None:
            self.delete_edge(node_start, node_end)

        edges = self._graph[node_start]
        for edge in edges:
            if edge[0] == node_end:
                edge[1] = weight

    @property
    def nodes(self):
        '''
            returns a list of all nodes
        '''
        return [*self._graph]

    @property
    def graph(self):
        '''
            returns the graph
        '''
        return self._graph

    def return_edges(self, node):
        if node not in self._graph:
            raise ValueError("The Node does not exist")
        else:
            return self._graph[node]
