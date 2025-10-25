from network_elements import *
from system import System


class Command:
    def execute(self):
        ...

    def can_undo(self):
        ...

    def can_redo(self):
        return False

    def undo(self):
        return False


class AddNetwork(Command):
    def __init__(self, system, net_name, net_address):
        self.system = system
        self.net_name = net_name
        self.net_address = net_address
        super().__init__()

    def execute(self):
        self.system.add_connection(self.net_name, self.net_address)

    def can_undo(self):
        return self.system.has_connection(self.net_name)

    def can_redo(self):
        return not self.system.has_connection(self.net_name)

    def undo(self):
        self.system.remove_connection(self.net_name)


class RemoveNetwork(Command):
    def __init__(self, system, net_name):
        self.system = system
        self.net_name = net_name
        self.connection = ""
        super().__init__()

    def execute(self):
        self.connection = self.system.get_connection(self.net_name)
        self.system.remove_connection(self.net_name)

    def can_undo(self):
        return not self.system.has_connection(self.net_name)

    def can_redo(self):
        return self.system.has_connection(self.net_name)

    def undo(self):
        address = self.connection.network.network_address
        self.system.add_connection(self.connection.name, address)


class WriteConfig(Command):
    def __init__(self, system):
        self.system = system
        super().__init__()

    def execute(self):
        self.system.write_config_file()

    
def WriteKathara(Command):
    def __init__(self, system):
        self.system = system
        super().__init__()
        
    def execute(self):
        self.system.write_kathara_config()
        
    
class AddRouter(Command):
    def __init__(self, system, name, connections = [], routes = []):
        self.system = system
        self.name = name
        self.connections = connections
        self.routes = routes
        
    def execute(self):
        self.system.add_router(self.name, self.connections, self.routes)
        
        
class RemoveRouter(Command):
    def __init__(self, system, name):
        self.system = system
        self.name = name
        self.router = None
        
    def execute(self):
        self.router = self.system.get_router(self.name)
        self.system.remove_router(self.name)
        
    def can_undo(self):
        return False

class AddRoute(Command):
    def __init__(self, system, name, via, con_name):
        self.system = system
        self.name = name
        self.via = via
        self.con_name = con_name
        super().__init__()
        
    def execute(self):
        self.system.add_route(self.name, self.via, self.con_name)
        
class RemoveRoute(Command):
    def __init__(self, system, name, via, con_name):
        self.system = system
        self.name = name
        self.via = via
        self.con_name = con_name
        super().__init__()
        
    def execute(self):
        self.system.remove_route(self.name, self.via, self.con_name)
        

class Invoker:
    def __init__(self):
        self.commandStack = []
        self.undidStack = []

    def add_command(self, command):
        self.commandStack.append(command)

    def add_undid(self, command):
        self.undidStack.append(command)

    def execute_top(self):
        self.top_stack().execute()

    def undo_top(self):
        if self.top_stack().can_undo():
            self.top_stack().undo()
            self.add_undid(self.top_stack())
            self.commandStack.pop()
        else:
            self.commandStack.pop()

    def redo_top(self):
        if self.top_undid().can_redo():
            self.top_undid().execute()
            self.add_command(self.top_undid())
            self.undidStack.pop()
        else:
            self.undidStack.pop()

    def top_stack(self):
        return self.commandStack[len(self.commandStack) - 1]

    def top_undid(self):
        return self.undidStack[len(self.undidStack) - 1]
