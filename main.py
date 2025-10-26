"""
Converts Json to linux ip routes
The first Connection in the arrays of host or routers is its local network
"""

from commands import *
from system import System


HELP = """WRITE KATHARA -> Write Kathara configs
WRITE CONFIG -> Write the json config file
ADD NET -> Add a network/connection
RM NET -> Remove a network/connection
ADD HOST -> Add a host TODO
RM HOST -> Remove a host TODO
ADD ROUTER -> Add a router
RM ROUTER -> Remove a router
ADD ROUTE -> Add a route to a router
RM ROUTE -> Remove a route from a router
ADD CONH -> Add a connection to a host
RM CONH -> Remove a connection to a host
ADD CONR -> Add a connection to a router
RM CONR -> Remove a connection to a router

UNDO -> Undo last action
REDO -> Redo last undone action

HELP -> Show this menu

EXIT -> Exit program
SEXIT -> Write config file and exit program
"""


def main():
    system = System("config.json")
    invoker = Invoker()

    try:
        while True:
            cmd = input(">>>>").upper()
            if cmd == "WRITE KATHARA":
                system.write_kathara_config()
            elif cmd == "WRITE CONFIG":
                c = WriteConfig(system)
                invoker.add_command(c)
                invoker.execute_top()
            elif cmd == "ADD NET":
                c = AddNetwork(system, input("Network Name>>>>"), input("Network Address>>>>"))
                invoker.add_command(c)
                invoker.execute_top()
            elif cmd == "RM NET":
                c = RemoveNetwork(system, input("Network Name>>>>"))
                invoker.add_command(c)
                invoker.execute_top()
            elif cmd == "ADD HOST":
                ...
            elif cmd == "ADD ROUTER":
                c = AddRouter(system, input("Router Name>>>>"))
                invoker.add_command(c)
                invoker.execute_top()
            elif cmd == "RM ROUTER":
                c = RemoveRouter(system, input("Router Name>>>>"))
                invoker.add_command(c)
                invoker.execute_top()
            elif cmd == "ADD ROUTE":
                c = AddRoute(system, input("Router Name>>>>"),
                             input("Via Router>>>>"),
                             input("Connection Name>>>>"))
                invoker.add_command(c)
                invoker.execute_top()
            elif cmd == "RM ROUTE":
                c = RemoveRoute(system, input("Router Name>>>>"),
                             input("Via Router>>>>"),
                             input("Connection Name>>>>"))
                invoker.add_command(c)
                invoker.execute_top()
            elif cmd == "ADD CONH":
                c = AddConnectionHost(system, input("Host Name>>>>"),
                                      input("Connection Name>>>"))
                invoker.add_command(c)
                invoker.execute_top()
            elif cmd == "RM CONH":
                c = RemoveConnectionHost(system, input("Host Name>>>>"),
                                      input("Connection Name>>>"))
                invoker.add_command(c)
                invoker.execute_top()
            elif cmd == "ADD CONR":
                c = AddConnectionRouter(system, input("Router Name>>>>"),
                                      input("Connection Name>>>"))
                invoker.add_command(c)
                invoker.execute_top()
            elif cmd == "RM CONR":
                c = RemoveConnectionRouter(system, input("Router Name>>>>"),
                                      input("Connection Name>>>"))
                invoker.add_command(c)
                invoker.execute_top()
            elif cmd == "EXIT":
                break
            elif cmd == "SEXIT":
                c = WriteConfig(system)
                invoker.add_command(c)
                invoker.execute_top()
                break
            elif cmd == "HELP":
                print(HELP)
            elif cmd == "PRINT":
                ...
            elif cmd == "UNDO":
                invoker.undo_top()
            elif cmd == "REDO":
                invoker.redo_top()
            else:
                print("Unknown")
    except Exception as e:
        print(e)
        

if __name__ == "__main__":
    main()