from copy import deepcopy

class Graph:
    def __init__(self, graph = None):
        if graph == None:
            self.__graph = {}
        else:
            self.__graph = graph

    def vertices(self):
        return self.__graph

    def edges(self, vertex):
        return self.__graph[vertex]

    def add_vertex(self, vertex):
        if vertex not in self.__graph:
            self.__graph[vertex] = []

    def rem_vertex(self, vertex):
        for v in self.__graph[vertex]:
            self.__graph[v].remove(vertex)
        del self.__graph[vertex]

    def add_edge(self, edge):
        edge = set(edge)
        (vertex1,vertex2) = tuple(edge)

        if vertex1 in self.__graph and vertex2 in self.__graph[vertex1]:
            return

        if vertex1 in self.__graph:
            self.__graph[vertex1].append(vertex2)
        else:
            self.__graph[vertex1] = [vertex2]

        if vertex2 in self.__graph:
            self.__graph[vertex2].append(vertex1)
        else:
            self.__graph[vertex2] = [vertex1]

    def __edges(self):
        edges = []
        for vertex in self.__graph:
            for neighbour in self.__graph[vertex]:
                #if {neighbour, vertex} not in edges:
                edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        #return str(self.__graph)
        s = "V: "
        for v in self.__graph:
            s += str(v) + " -> "
            s += ",".join(self.__graph[v])
            s += "\n"
        return s

    def components(self):
        number_cmp = 0
        components = {number_cmp : []}
        vertices_visited = set([item for sublist in components.values() for item in sublist])
        while set(self.__graph.keys()) != vertices_visited:
            for vertex in self.__graph:
                if vertex not in vertices_visited:
                    if number_cmp not in components:
                        components[number_cmp] = []
                    components[number_cmp].append(vertex)
                    self.__component_recursive(self.__graph[vertex], components[number_cmp])
                    vertices_visited = set([item for sublist in components.values() for item in sublist])
                    number_cmp +=1

        subgraphs = []
        for component in components.values():
            graph = Graph()
            for vertex in component:
                graph.add_vertex(vertex)
                #print(self.edges(vertex))
                for vertex_adj in self.edges(vertex):
                    graph.add_edge((vertex, vertex_adj))
            subgraphs.append(graph)

        return subgraphs

    def __component_recursive(self, vertices, component):
        for vertex in vertices:
            if vertex not in component:
                component.append(vertex)
                self.__component_recursive(self.__graph[vertex], component)

    def number_components(self):
        #print(self.__graph)
        return len(self.components())

    def tree(self, vertex):
        """
        Function to start recursively dfs on graph structure

        Args:
            vertex: input vertex, considered as root vertex
        Output:
            dictionary tree with vertices from graph
            {#vertex, (#level, [#adjacents])}
        """

        vertices = list(self.__graph.keys())
        vertices.remove(vertex)
        level = 0

        return self.__tree_recursive(vertex, vertices, level)

    def __tree_recursive(self, vertex, vertices, level):
        """
        Args:
            vertex: input vertex
            vertices: vertices not visited
            level: to identify the level of vertex
        Output:
            dictionary tree with vertices from graph
            {#vertex, (#level, [#adjacents])}
        """
        dict_tree = {}
        vert_visited = []
        for adjacent in self.__graph[vertex]:
            if adjacent in vertices:
                vertices.remove(adjacent)
                vert_visited.append(adjacent)
                dict_tree[vertex] = (level, vert_visited)
                ret = self.__tree_recursive(adjacent, vertices, level + 1)
                dict_tree = {**dict_tree, **ret}


        if dict_tree == {}:
            dict_tree[vertex] = (level, [])

        return dict_tree

    def lowpoint(self, tree):
        """
        Args:
            tree: tree massa
        Output:
            dictionary tree with vertices from graph
            {#vertex, #lowpoint}
        """
        dict_lwpt = {}
        root = list(tree.keys())[0]
        dict_lwpt[root] = root
        for vertex in tree:
            level, adjs = tree[vertex]
            for adj in adjs:
                dict_lwpt[adj] = vertex

        for vertex in dict_lwpt:
            lvl, adjs = tree[dict_lwpt[vertex]]
            if lvl > 0 :
                for adj in self.__graph[vertex]:
                    new_lvl, new_vertex = (tree[adj][0], adj)
                    if new_lvl < lvl:
                        dict_lwpt[vertex] = new_vertex


        return dict_lwpt

    def articulation(self, tree, lowpoint):
        """
        Args:
            tree: tree massa
            lowpoint: lowpoint
        Output:
            dictionary tree with vertices from graph
            {#vertex, #lowpoint}
        """
        art = []

        root = list(tree.keys())[0] #pega a rais do dict_tree
        level, childs = tree[root]
        if(len(childs) > 1):
            art.append(root)

        for vertex in tree:
            if vertex != root:
                for adj in tree[vertex][1]:
                    if lowpoint[adj] == vertex or lowpoint[adj] == adj:
                        art.append(vertex)
                        break

        return art


    def demarker(self, tree, lowpoint):
        """
        Args:
            tree: tree massa
            lowpoint: lowpoint
        Output:
            dictionary demarker with vertices from graph
            {#vertex, #lowpoint}
        """
        dkr = []

        root = list(tree.keys())[0] #pega a rais do dict_tree
        level, childs = tree[root]
        dkr = deepcopy(childs)

        for vertex in tree:
            if vertex != root and vertex not in childs:
                for adj in tree[vertex][1]:
                    if lowpoint[adj] == vertex or lowpoint[adj] == adj:
                        dkr.append(adj)

        return dkr

    def subtree(self, tree, vertex):
        dict_tree = {}
        dict_tree[vertex] = deepcopy(tree[vertex])
        for adj in tree[vertex][1]:
            ret = self.subtree(tree, adj)
            dict_tree = {**dict_tree, **ret}
        return dict_tree

    def subtree_has_articulation(self, subtree, articulations):
        for vertex in subtree:
            if vertex in articulations:
                return True

        return False


    def biconnected_component(self, tree, articulations, demarkers):
        bcc = []
        tree = deepcopy(tree)
        while demarkers:
            for demark in demarkers:
                subtree = self.subtree(tree, demark)
                if self.subtree_has_articulation(subtree, articulations):
                    continue
                vertex = None
                for v in articulations:
                    if demark in tree[v][1]:
                        vertex = v
                        break

                bcc.append([vertex] + list(subtree.keys()))
                print(bcc)
                demarkers.remove(demark)

                for leaf in subtree:
                    del tree[leaf]
                    for leaf2 in tree:
                        if leaf in tree[leaf2][1]:
                            tree[leaf2][1].remove(leaf)

                if set(tree[v][1]).intersection(set(demarkers)) == set():
                    articulations.remove(v)

                input()
        return bcc










if __name__ == "__main__":
    g = { "a" : ["b","c"],
            "b" : ["a", "d"],
            "c" : ["a"],
            "d" : ["b","e"],
            "e" : ["d"],
            "g" : ["h", "i"],
            "h" : ["g"],
            "i" : ["g"]}

    h = { '1' : ['2','8','9','10'],
            '2' : ['1','3','4','5','8','10'],
            '3' : ['2','4','5'],
            '4' : ['2','3','5'],
            '5' : ['2','3','4'],
            '6' : ['7','8'],
            '7' : ['6','8'],
            '8' : ['1','2','6','7','9'],
            '9' : ['1','8'],
            '10' : ['1','2']}


    graph = Graph(h)
    print(graph)
    c = graph.components()[0]
    t = c.tree("8")
    lp = graph.lowpoint(t)
    print("tree")
    print(t)
    print("low point")
    print(lp)
    ar = graph.articulation(t, lp)
    print("articulation")
    print(ar)
    dkr = graph.demarker(t, lp)
    print("demarker")
    print(dkr)
    sbt = graph.subtree(t, "1")
    print(sbt)
    print("bbc")
    bbc = graph.biconnected_component(t,ar,dkr)
    #v = graph.cut_vertices()
    #print(v)
    #graph.components()
    #graph.rem_vertex('b')
    #print(graph.number_components())
    #print(graph)
    #graph.add_edge({'x','y'})
    #graph.add_edge({'a','y'})
    #print(graph)
