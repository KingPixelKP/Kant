import json

from network_elements import Host, Router, Connection

def get_common_connection(router1, router2):
    for connection1 in router1.connections:
        for connection2 in router2.connections:
            if connection1 == connection2:
                return connection1
    raise ValueError("No Common Connection Found")

class System:
    ...
    def __init__(self, config_file):
        self.config_file = config_file
        self.nodes, self.hosts, self.routers, self.connections = self.read_conf()
        #self.sanity_check()

    def sanity_check(self):
        for _, v in self.nodes.items():
            for dev in v["connected"]:
                if self.connections.get(dev) is None:
                    raise ValueError("Inexistent Device")

    def read_conf(self) -> tuple[dict, dict, dict, dict]:
        with open(self.config_file) as f:
            buffer = f.read()
            config = json.loads(buffer)
            hosts = config["hosts"]
            routers = config["routers"]
            networks = config["networks"]
            nodes = {}
            nodes.update(config["hosts"])
            nodes.update(config["routers"])

        hosts_dict = {}
        routers_dict = {}
        networks_dict = {}


        for k,v in hosts.items():
            hosts_dict[k] = Host(k, v["connected"], v["gateway"])

        for k,v in routers.items():
            routers_dict[k] = Router(k, v["connected"], v["routes"])

        for k,v in networks.items():
            networks_dict[k] = Connection(k, v["network"])

        nodes = {}
        nodes.update(hosts_dict)
        nodes.update(routers_dict)

        return nodes, hosts_dict, routers_dict, networks_dict

    def write_conf(self):
        with open("lab.conf", "w") as f:
            for k, v in self.nodes.items():
                f.write(f"#{k}\n")
                i = 0
                for con in v.connections:
                    f.write(f"{k}[{i}]={con}\n")
                    i += 1
                f.write("\n")

    def write_connection_ips(self):
        for k,v in self.nodes.items():
            with open(f"{k}.startup", "w") as f:
                f.write(f"#{k}\n")
                i = 0
                for conName in v.connections:
                    f.write(f"#Ip address in {conName}\n")
                    f.write(f"ip addr add {self.connections[conName].get_current_available_ip()}/{self.connections[conName].network.prefixlen} dev eth{i}\n")
                    self.connections[conName].add_node(v)
                    f.write("\n")
                    i += 1

    def write_default_gateways(self):
        for k, v in self.hosts.items():
            with open(f"{k}.startup", "a") as f:
                f.write(f"#Default Gateway {v.gateway}\n")
                i = 0
                for conNam in v.connections:
                    gateway_ip = self.connections[conNam].nodes[v.gateway][1]
                    f.write(f"ip route add default via {gateway_ip} dev eth{i}\n")
                    i += 1

    def write_routes(self):
        for routerName, router in self.routers.items():
            with open(f"{routerName}.startup", "a") as f:
                for route in router.routes:
                    via_router = self.routers[route["router"]]
                    dest_network = self.connections[route["destNetwork"]]
                    dest_network_ip = dest_network.network
                    router_network = self.connections[get_common_connection(router, via_router)]
                    via_router_ip = router_network.nodes[via_router.name][1]
                    f.write(f"#Using {via_router.name}, in network {router_network.name}, to go to network {dest_network.name}\n")
                    f.write(f"ip route add {dest_network_ip} via {via_router_ip} dev eth{router.connections.index(router_network.name)}\n\n")

    def write_kathara_config(self):
        self.write_conf()
        self.write_connection_ips()
        self.write_default_gateways()
        self.write_routes()
        print("Wrote Kathara config files")

    def write_config_file(self):
        with open(self.config_file, "w") as f:
            f.write("{")
            self.write_hosts(f)
            f.write(",")
            self.write_routers(f)
            f.write(",")
            self.write_networks(f)

            f.write("}")

        print("Wrote config file")

    def write_hosts(self, f):
        f.write('"hosts":{')
        i = 0
        for _, v in self.hosts.items():
            f.write(v.__json__())
            i += 1
            if i != len(self.hosts):
                f.write(",")

        f.write('}')

    def write_routers(self, f):
        f.write('"routers":{')
        i = 0
        for _, v in self.routers.items():
            f.write(v.__json__())
            i += 1
            if i != len(self.routers):
                f.write(",")
        f.write('}')

    def write_networks(self, f):
        f.write('"networks":{')
        i = 0
        for _, v in self.connections.items():
            f.write(v.__json__())
            i += 1
            if i != len(self.connections):
                f.write(",")
        f.write("}")

    def get_connection(self, name) -> Connection:
        return self.connections.get(name)
    
    def has_connection(self, name) -> bool:
        return self.get_connection(name) is not None

    def add_connection(self, name, network):
        if self.has_connection(name):
            raise ValueError("Connection Already Exists")

        self.connections[name] = Connection(name, network)

    def remove_connection(self, name):
        if not self.has_connection(name):
            raise ValueError("Connection does not Exist")

        self.connections.pop(name)
        
    def get_router(self, name) -> Router:
        return self.routers.get(name)
    
    def has_router(self, name) -> bool:
        return self.get_router(name) is not None
    
    def add_router(self, name, connections = [], routes = []):
        if self.has_router(name):
            raise ValueError("Router already exists")
        
        self.routers[name] = Router(name, connections=connections, routes=routes)
        
    def remove_router(self, name):
        if not self.has_router(name):
            raise ValueError("Router does not exist")
        
        self.routers.pop(name)

    def add_route(self, name, via, con_name):
        if not self.has_router(name):
            raise ValueError("Router does not exist")
        
        router = self.get_router(name)
        router.add_route(via, con_name)
        
    def remove_route(self, name, via, con_name):
        if not self.has_router(name):
            raise ValueError("Router does not exist")
        
        router = self.get_router(name)
        router.remove_route(via, con_name)
        