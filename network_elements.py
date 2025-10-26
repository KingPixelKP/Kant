import ipaddress
import json


class Node:

    def __init__(self, name, connections):
        self.name = name
        self.connections : list = connections
        
    def has_connection(self, con_name):
        try:
            self.connections.index(con_name)
            return True
        except Exception:
            return False
        
    def add_connection(self, con_name):
        if self.has_connection(con_name):
            raise ValueError("Connection already existent")
        
        self.connections.append(con_name)
        
    def remove_connection(self, con_name):
        if not self.has_connection(con_name):
            raise ValueError("Connection does not exist")
        
        self.connections.append(con_name)
    


class Host(Node):


    def __init__(self, name, gateway, connections = []):
        self.gateway = gateway
        super().__init__(name, connections)

    def __str__(self):
        return f"Host: {self.name}, Connections: {self.connections}, Gateway: {self.gateway}"

    def __json__(self):
        return f'"{self.name}" : {{"connected": {json.dumps(self.connections)},"gateway":{json.dumps(self.gateway)}}}'


class Router(Node):
    def __init__(self, name, connections = [], routes = []):
        self.routes : list = routes
        super().__init__(name, connections)

    def __str__(self):
        routes = ""

        for ele in self.routes:
            routes += f'Router: {ele["router"]}, Destination Network: {ele["destNetwork"]}\n'

        if routes == "":
            return f"Routers: {self.name}, Connections {self.connections}"
        else:
            return f"Routers: {self.name}, Connections {self.connections}\nRoutes:\n{routes}"

    def __json__(self):
        routes = "["
        i = 0
        for route in self.routes:
            routes += f'{{"router": "{route["router"]}", "destNetwork":"{route["destNetwork"]}"}}'
            i += 1
            if i != len(self.routes):
                routes += ","

        routes += "]"

        return f'"{self.name}": {{"connected":{json.dumps(self.connections)}, "routes": {routes}}}'
    
    def has_route(self, via, con_name):
        try:
            self.routes.index({"router":via, "destNetwork":con_name}) 
            return True
        except:
            return False 
    
    def add_route(self, via, con_name):
        if self.has_route(via, con_name):
            raise ValueError("Route alreay existent")
        self.routes.append({"router":via, "destNetwork":con_name})
        
    def remove_route(self, via, con_name):
        if not self.has_route(via, con_name):
            raise ValueError("Route does not exist")
        self.routes.remove({"router":via,"destNetwork":con_name})


class Connection:


    def __init__(self, name, network):
        self.nodes = {}
        self.name = name
        self.network = ipaddress.ip_network(network)


    def add_node(self, node : Node):
        self.nodes[node.name] = (node, self.network[len(self.nodes) + 1])

    def get_current_available_ip(self):
        return self.network[len(self.nodes) + 1]

    def __str__(self):
        nodes = ""
        for k, v in self.nodes.items():
            nodes += f"Node: {k}, Address: {v[1]}\n"

        if nodes == "":
            return f"Connection: {self.name}, Network: {self.network}"
        else:
            return f"Connection: {self.name}, Network: {self.network}\nNodes:\n{nodes}"

    def __json__(self):
        return f'"{self.name}":{{"network":"{self.network}"}}'
